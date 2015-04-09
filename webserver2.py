from flask import Flask, render_template, request
import datetime
from classify import classify, get_duration_formatted, load_json_dump
from random_forests import create_model, rf_classify
from youtube import download_youtube
import json
from pymongo import MongoClient
import glob
from threading import Thread
from flask_cors import CORS
from sklearn.externals import joblib

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def main():
	return render_template('main.html')


@app.route("/musicplayer")
def player():
	return render_template('player.html')

@app.route("/playlist")
def playlist_():
	playlist = json.dumps(load_json_dump('classified_songs.json').values())
	print 'playlist loaded: ', playlist
	return playlist


json_dump = {}
try:		
	json_dump = load_json_dump('classified_songs.json')
except:
	json_dump = {}
def do_job(artist, title):
	if title == '':
		title = 'Unknown'
	if artist == '':
		artist == 'Unknown'
	status, song = download_youtube(artist, title)
        labels, probabilities, genre = rf_classify(song, predictor)
        json_dump[song] = {'filename': song, 'genre': genre[0], 'mp3': song, 'confidence': max(probabilities[0]), 'title': title, 'artist': artist, 'duration': get_duration_formatted(song), 'rating': 4}		 	

	with open('classified_songs.json', 'w') as outfile:
		json.dump(json_dump, outfile, indent=4, sort_keys=True)

def create_worker(artist, title):
	Thread(target = do_job, args = (artist, title)).start()

@app.route('/download', methods=['POST'])
def download():
	try:
		if request.method == 'POST':
			title = request.form['title']
			artist = request.form['artist']
			create_worker(artist, title)
			return render_template('downloading.html')
	except:
		pass
	else:
		return 404

@app.route('/voice', methods=['POST'])
def voice():
	try:
		if request.method == 'POST':
			title = request.form['title']
			artist = request.form['artist']
			create_worker(artist, title)
			return "200"
	except Exception as e:
		print e
		pass
	else:
		return 404


if __name__ == "__main__":
	try:
		predictor = joblib.load('serialized_model/serialized_model.pkl')
	except:
		print 'Failed to load serialized model.'
		predictor = create_model()
		joblib.dump(predictor, 'serialized_model/serialized_model.pkl')
	app.run(threaded=True, host = '0.0.0.0', port=8080 , debug = True, use_reloader=False)

