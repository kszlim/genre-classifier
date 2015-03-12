import librosa
import numpy as np
import json
import glob
import os
import matplotlib.pyplot as plt
from collections import Counter
from math import sqrt
from config import directories, genres


class NumpyAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray) and obj.ndim == 1:
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def squared_euclidean(arr1, arr2):
	distance_squared = 0
	for index, x in enumerate(arr1):
		distance_squared += (x - arr2[index])**2
	return sqrt(distance_squared)

def get_filepaths(base_directory):
	return (base_directory.split('/')[-2], glob.glob(base_directory + '*.mp3') + glob.glob(base_directory + '*.m4a') + glob.glob(base_directory + '*.flac'))

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

def create_json_dump(output_path='training_data/data.json', pretty=False):
	data = {}
	for directory in directories:
		genre, filepaths = get_filepaths(directory)
		data[genre] = {}
		for index, filepath in enumerate(filepaths):
			print 'Done: ' + str(index)
			try:
				fft_data, sample_rate, bins = get_fft(filepath)
				data[genre][os.path.basename(filepath)] = {'raw_fft_data': fft_data, 'sample_rate': sample_rate, 'bins': bins}
			except:
				continue
	with open(output_path, 'w') as outfile:
		if pretty:
			json.dump(data, outfile, cls=NumpyAwareJSONEncoder, indent=4, sort_keys=True)
		else:
			json.dump(data, outfile, cls=NumpyAwareJSONEncoder)

def load_json_dump(input_path='training_data/data.json'):
	with open(input_path, 'r') as infile:
		string_json = infile.read()
	return json.loads(string_json)

def plot_averages(genres=genres, data=load_json_dump()):
	for genre in genres:
		genre_data = []
		for song in data[genre].values():
			genre_data.append(song['raw_fft_data'])
		genre_data = np.array([sum(x) for x in zip(*genre_data)])
		scale = sum(genre_data)
		genre_data = genre_data*10000/scale
		plt.bar(data[genre].values()[0]['bins'], genre_data)
		axes = plt.gca()
		axes.set_ylim([0, 500])
		fig = plt.gcf()
		fig.set_size_inches(18.5,10.5)
		fig.savefig('plots/' + genre + '_bar.png')
		plt.clf()

def linear_bins(raw_fft):
	binned_fft = []
	index = 0
	while(len(binned_fft) < 8):
		binned_fft.append(sum(raw_fft[index:index+32:]))
		index += 32
	return binned_fft

def logarithmic_bins(raw_fft):
	binned_fft = []
	index = 0
	n = 1
	while(len(binned_fft) < 8):
		binned_fft.append(sum(raw_fft[index:index+n:])/n)
		index += n
		n = n*2
	return binned_fft

def normalize(input_list, n=10000):
	scale = sum(input_list)/n
	return [x/scale for x in input_list]

def generate_bin_from_song(binning_function, genre, song):
	binned_fft = normalize(binning_function(song['raw_fft_data']))
	return {'binning_type': binning_function.__name__, 'genre': genre, 'binned_data': binned_fft}

def generate_bins(bin_type = linear_bins, fft_data=load_json_dump(), output_path='training_data.json', pretty=False):
	
	def dump_data(data, output_path=output_path, folder=''):
		with open(folder + '/' + bin_type.__name__ + '_' + output_path, 'w') as outfile:
			if pretty:
				json.dump(data, outfile, indent=4, sort_keys=True)
			else:
				json.dump(data, outfile)	

	training_data = []
	test_data = []
	for genre in genres:
		songs = fft_data[genre].values()
		number_songs = len(songs)
		print number_songs, genre, len(fft_data[genre])
		for index, song in enumerate(songs):
			if index % 6 == 0: 
				training_data.append(generate_bin_from_song(bin_type, genre, song))
			else:
				test_data.append(generate_bin_from_song(bin_type, genre, song))

	dump_data(training_data, folder='training_data')
	dump_data(test_data, 'test_data.json', folder='test_data')
	

def knn(input_data, training_data, k=11):
	knn_results = []
	for training_value in training_data:
		knn_results.append({'euclidean': squared_euclidean(input_data, training_value['binned_data']), 'genre': training_value['genre']})
	return sorted(knn_results, key=lambda x: x['euclidean'])[:k:]

def majority_vote(knn_output):
	count = Counter()
	for result in knn_output:
		count[result['genre']] += 1
	return count.most_common(1)[0][0], count

def weighted_vote(knn_output):
	count = Counter()
	for result in knn_output:
		if result['euclidean'] == 0.0:
			count[result['genre']] += 1	
		else:
			count[result['genre']] += 1/(float(result['euclidean'])**2)
	return max(count, key=count.get), count

def cross_validate(bin_types=['logarithmic_bins', 'linear_bins']):

	def create_counter():
		return {genre: {'success': 0, 'failure': 0, 'total': 0} for genre in genres}

	final_results = {}

	all_tests = []

	for bin_type in bin_types:
		test_data = load_json_dump('test_data/' + bin_type +  '_test_data.json')
		training_data = load_json_dump('training_data/' + bin_type + '_training_data.json')

		for k in range(1, 15):
			results = create_counter()
			results['k-value'] = k

			for genre in genres:
				results[genre]['misclassified_as'] = Counter()

			for test_value in test_data:
				
				#print test_value
				knn_output = knn(test_value['binned_data'], training_data, k)
				result_genre = test_value['genre']
				
				#Voting scheme
				guessed_genre, count = majority_vote(knn_output)
				
				test_cases = (k, bin_type, ('actual genre', result_genre), ('guessed_genre', guessed_genre), count.most_common(), knn_output)
				all_tests.append(test_cases)

				if guessed_genre == result_genre:
					results[result_genre]['success'] += 1
					results[result_genre]['total'] += 1
				else:
					results[result_genre]['total'] += 1
					results[result_genre]['failure'] += 1
					results[result_genre]['misclassified_as'][guessed_genre] += 1
			for genre in genres:
				results[genre]['Accuracy'] = float(results[genre]['success'])/results[genre]['total']
			
			for genre in genres:
				results[genre]['misclassified_as'] = {k: v for k, v in results[genre]['misclassified_as'].iteritems()}

			final_results[str(k) + '_' + bin_type] = results
	return final_results, all_tests

def classify(path, binning_function=logarithmic_bins):
	results = knn(normalize(binning_function(get_fft(path, window_length=1024)[0])), load_json_dump('training_data/' + 'logarithmic_bins_training_data.json'), k=9)
	count = Counter()
	for result in results:
		count[result['genre']] += 1
	return count.most_common(1)[0][0], results

def classify_directory(directory):
	test_files = get_filepaths(directory)[1]
	count = Counter()
	for test_file in test_files:
		try:
			genre, results = classify(test_file)
			count[genre] += 1
		except:
			continue
	return count
	
def test_results():
	results, all_tests = cross_validate()

	summarized_results = []

	for k, result in results.iteritems():
		counter = Counter()
		for genre in genres:
			counter['success'] += result[genre]['success']
			counter['total'] += result[genre]['total']
		summarized_results.append((k, float(counter['success'])/counter['total']))

	print sorted(summarized_results, key=lambda x: x[1])

	with open('results/results.json', 'w') as outfile:
		json.dump(results, outfile, indent=4, sort_keys=True)

	with open('results/all_tests.txt', 'w') as outfile:
		outfile.writelines([str(test) +'\n' for test in all_tests])

def regenerate_data():
	create_json_dump()
	generate_bins()
	generate_bins(logarithmic_bins)

test_results()
