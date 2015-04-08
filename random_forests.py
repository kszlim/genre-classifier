from sklearn.ensemble import RandomForestClassifier
from classify import load_json_dump, normalize, get_fft2, get_fft
from sklearn.neighbors import KNeighborsClassifier
import re
import numpy as np


def create_classifier_and_fit(data, labels):
	forest = RandomForestClassifier(n_estimators = 1000, n_jobs=-1)
	forest.fit(data, labels)
	return forest

def create_data(raw_data = load_json_dump('training_data/data.json')):
	data = []
	labels = []
	for key in raw_data:
		for song in raw_data[key].values():
			data.append(normalize(song['raw_fft_data']))
			labels.append(key)
	return data, labels

def create_song_data(file_name, raw_data = load_json_dump('training_data/data3.json')):
	data = []
	labels = []
	for key in raw_data:
		for song_title, song in raw_data[key].iteritems():
			if song_title.startswith(file_name):
				data.append(normalize(song['raw_fft_data']))
				labels.append(key)
	return data, labels

def format_binned_data(path):
	raw_data = load_json_dump(path)
	data = []
	labels = []
	for song in raw_data:
		labels.append(song['genre'])
		data.append(song['binned_data'])
	return data, labels

def create_model():
	data, labels = create_data()
	return create_classifier_and_fit(data, labels)

def create_summed_model():
	data, labels = create_data(raw_data = load_json_dump('training_data/data2.json'))
	return create_classifier_and_fit(data, labels)

def create_model_2():
	data, labels = format_binned_data('training_data/logarithmic_bins_training_data.json')
	return create_classifier_and_fit(data, labels)

def create_model_3():
	data, labels = format_binned_data('training_data/logarithmic_bins_training_data.json')
	knn = KNeighborsClassifier(9).fit(data, labels)
	return knn

def create_model_4():
	data, labels = create_data()
	data = data[::2]
	labels = labels[::2]
	knn = KNeighborsClassifier(9).fit(data, labels)
	return knn

def rf_classify(path, predictor):
	data, sr, bins = get_fft(path)
	data = normalize(data)
	return (predictor.classes_, predictor.predict_proba(data), predictor.predict(data))

def summed_classification2(path, predictor):
	data, sr, bins = get_fft2(path)
	data = [normalize(sample) for sample in data]
	return np.sum(predictor.predict_proba(data), axis=0), predictor.classes_

def get_class2(path, predictor):
	summed_probs, classes = summed_classification(path, predictor)
	return classes[summed_probs.argmax()]