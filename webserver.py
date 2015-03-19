from flask import Flask, render_template, request
import datetime
from classify import classify, get_duration_formatted, load_json_dump
from youtube import download_youtube
import json
from pymongo import MongoClient
import glob
from threading import Thread

app = Flask(__name__)
db = MongoClient()['genre-classifier']

button = {
	1 :{'name':'item x','state':"False"},
	2 :{'name':'item y','state':"False"},
	3 :{'name':'item z','state':"False"},
	4 :{'name':'item u','state':"False"}
	}
@app.route("/")
def main():
	
	templateData = {
		'button' : button
	}
	return render_template('main.html', **templateData)

@app.route("/1/<state>")
def button1(state):
	optionName = button[1]['name']
	if button[1]['state'] == "True":
		button[1]['state'] = "False"
		message = optionName + " is running."
	elif button[1]['state'] == "False":
		button[1]['state'] = "True"
		message = optionName + " is closed."
	templateData = {
		'button' : button,
		'message' : message
	}
	return render_template('main.html', **templateData)


@app.route("/2/<state>")
def button2(state):
	optionName = button[2]['name']
	if button[2]['state'] == "True":
		button[2]['state'] = "False"
		message = optionName + " is running."
	elif button[2]['state'] == "False":
		button[2]['state'] = "True"
		message = optionName + " is closed."
	templateData = {
		'button' : button,
		'message' : message
	}
	return render_template('main.html', **templateData)

@app.route("/3/<state>")
def button3(state):
	optionName = button[3]['name']
	if button[3]['state'] == "True":
		button[3]['state'] = "False"
		message = optionName + " is running."
	elif button[3]['state'] == "False":
		button[3]['state'] = "True"
		message = optionName + " is closed."
	templateData = {
		'button' : button,
		'message' : message
	}
	return render_template('main.html', **templateData)


@app.route("/page1")
def page_one():
	return render_template('page_one.html')

@app.route("/musicplayer")
def player():
	return render_template('player.html')

@app.route("/playlist")
def playlist_():
	playlist = json.dumps(load_json_dump('classified_songs.json').values())
	print 'playlist loaded: ', playlist
	return playlist

def do_job(artist, title):
	download_youtube(artist, title)
	json_dump = {}
	try:		
		json_dump = load_json_dump('classified_songs.json')
	except:
		pass
	songs = glob.glob('static/downloaded_songs/*.mp3')
	for song in songs:
		if song not in json_dump:
			print song
		 	#genre, data = classify(song)
		 	#json_dump[song] = {'filename': song, 'genre': genre, 'mp3': song, 'title': title, 'artist': artist, 'duration': get_duration_formatted(song), 'rating': 4}
		 	json_dump[song] = {'filename': song, 'genre': 'rap', 'mp3': song, 'title': title, 'artist': artist, 'duration': '2:23', 'rating': 4}
		else:
		 	print 'didnot'

	with open('classified_songs.json', 'w') as outfile:
		json.dump(json_dump, outfile, indent=4, sort_keys=True)

def create_worker(artist, title):
	Thread(target = do_job, args = (artist, title)).start()

@app.route('/download', methods=['POST'])
def login():
    if request.method == 'POST':
	    title = request.form['title']
	    artist = request.form['artist']
	    create_worker(artist, title)
	    return render_template('downloading.html')
    else:
        return 404


if __name__ == "__main__":
	app.run(host = '0.0.0.0', port=5000, debug = True, use_reloader=False)

