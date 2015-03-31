from sklearn.ensemble import RandomForestClassifier
from classify import load_json_dump, normalize
from sklearn.neighbors import KNeighborsClassifier


def create_classifier_and_fit(data, labels):
	forest = RandomForestClassifier(n_estimators = 1000, n_jobs=-1)
	forest.fit(data, labels)
	return forest

def create_data(raw_data = load_json_dump()):
	data = []
	labels = []
	for key in raw_data:
		for song in raw_data[key].values():
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
	data = data[::2]
	labels = labels[::2]
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

test_data, test_labels = format_binned_data('test_data/logarithmic_bins_test_data.json')
test_data2, test_labels2 = create_data()
test_data2 = test_data2[1::2]
test_labels2 = test_labels2[1::2]

predictor = create_model()
print(predictor.score(test_data2, test_labels2))

# predictor = create_model_2()
# print(predictor.score(test_data, test_labels))

# predictor2 = create_model_4()
# print(predictor2.score(test_data2, test_labels2))