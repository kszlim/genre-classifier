import csv
import json

def load_json_dump(input_path):
	with open(input_path, 'r') as infile:
		string_json = infile.read()
	return json.loads(string_json)


training_data = load_json_dump('training_data/logarithmic_bins_training_data.json')
test_data = load_json_dump('test_data/logarithmic_bins_test_data.json')

fieldnames = ['genre', 'binned_data']

def clean_dict(data):
	cleaned_array = []
	for index, dictionary in enumerate(data):
		cleaned_dict = {}
		for key in dictionary:
			if key in fieldnames:
				if key == 'binned_data':
					for index2, freq_bin in enumerate(dictionary[key]):
						cleaned_dict[index2] = str(int(freq_bin))
				else:
					cleaned_dict[key] = data[index][key]
		cleaned_array.append(cleaned_dict)

	return cleaned_array

training_data = clean_dict(training_data)
test_data = clean_dict(test_data)

fieldnames = ['genre'] + range(8)

with open('data.csv', 'wb') as csvfile:
	
	# writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	# writer.writeheader()
	all_data = []
	for data in training_data:
		all_data += data.values()
		# writer.writerow(data)
	for data in test_data:
		all_data += data.values()
	
	results = ','.join(all_data)
	csvfile.write(results)
		# writer.writerow(data)