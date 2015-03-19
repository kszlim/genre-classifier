from flask import Flask, render_template, request
import datetime
from classify import classify
from youtube import download_youtube
import json


app = Flask(__name__)

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
	return json.dumps([{'genre': 'metal', 'mp3':'static/mix/1.mp3', 'title':'Sample', 'artist':'Sample', 'rating':4, 'buy':'#', 'duration':'0:29'}, {'mp3':'static/mix/1.mp3', 'title':'Sample', 'artist':'Sample', 'rating':4, 'buy':'#', 'duration':'0:29'}])

if __name__ == "__main__":
	app.run(host = '0.0.0.0', port=5000, debug = True, use_reloader=False)
