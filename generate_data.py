import librosa
import numpy as np
import json
import glob
import os

class NumpyAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray) and obj.ndim == 1:
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

directories = ['/home/kszlim/music/classical/', '/home/kszlim/music/pop/', '/home/kszlim/music/rap/', '/home/kszlim/music/metal/']

def squared_euclidean(arr1, arr2):
	distance_squared = 0
	for index, x in enumerate(arr1):
		distance_squared += (x - arr2[index])**2

def get_filepaths(base_directory):
	return (base_directory.split('/')[-2], glob.glob(base_directory + '*.mp3'))

def extract_samples(filepath, offset=60):
	data, sample_rate = librosa.load(filepath, sr=32000, offset=offset, duration=60.0)
	data_max, data_min = max(data) - min(data), min(data)
	data = (data - data_min)/(data_max)
	return data, sample_rate

def get_fft(filepath, window_length=1024):
	data, sample_rate = extract_samples(filepath)
	if data.shape[0] != 1920000:
		data, sample_rate = extract_samples(filepath, offset=20)
	assert(data.shape[0] == 1920000), filepath + ' does not contain correct number of samples.'
	data = data.reshape(-1, window_length)
	data = abs(np.fft.fft(data))
	data = np.sum(data, axis=0)
	freq = np.fft.fftfreq(window_length, d=1.0/sample_rate)
	data, sample_rate, bins = data[1:window_length/2 + 1:], sample_rate, freq[:window_length/2:]
	assert data.shape[0] == len(bins) 
	return data, sample_rate, bins

def create_json_dump(output_path='./data.json', pretty=False):
	data = {}
	for directory in directories:
		genre, filepaths = get_filepaths(directory)
		data[genre] = {}
		for index, filepath in enumerate(filepaths):
			print 'Done: ' + str(index)
			fft_data, sample_rate, bins = get_fft(filepath)
			data[genre][os.path.basename(filepath)] = {'raw_fft_data': fft_data, 'sample_rate': sample_rate, 'bins': bins}
	with open(output_path, 'w') as outfile:
		if pretty:
			json.dump(data, outfile, cls=NumpyAwareJSONEncoder, indent=4, sort_keys=True)
		else:
			json.dump(data, outfile, cls=NumpyAwareJSONEncoder)

create_json_dump(pretty=True)


#print get_filepaths(directories[0])

