import wit
import json
from firebase import firebase
import time
import requests

wit_access_token = 'IDWUGDNBHGWFLUYQJVWXAZ33YD73CTIJ'

def setup_db():
	return firebase.FirebaseApplication('https://381.firebaseio.com', None)

def setup_wit():
	wit.init()

def cleanup_wit():
	wit.close()

def listen(intents):
	while True:
		wit.voice_query_start(wit_access_token)
		time.sleep(6)
		response = json.loads(wit.voice_query_stop())
		print response
		if len(response['outcomes']) > 0 and response['outcomes'][0]['intent'] == 'start_listen':
			break

	shutdown = False
	print 'test'
	while not shutdown:
		print 'test2'
		wit.voice_query_start(wit_access_token)
		time.sleep(5)
		response = json.loads(wit.voice_query_stop())
		print 'test3'
		print response, 'respsssssssss'
		print('Response: {}'.format(response))
		for outcome in response['outcomes']:
			if outcome['intent'] in intents:
				if outcome['intent'] == 'youtube':
					print 'sending request'
					intents[outcome['intent']](outcome['entities']['search_query'][0]['value'])
				elif intents[outcome['intent']]() == True:
					return listen(intents)
				break

def create_intents(firebase=setup_db()):
	intents = {}

	def shutdown():
		return True

	def play_music():
		firebase.put('/player', 'status', {'status': 'play'})

	def pause_music():
		firebase.put('/player', 'status', {'status': 'pause'})

	def back_music():
		firebase.put('/player', 'status', {'status': 'back'})

	def next_music():
		print 'here'
		result = firebase.put('/player', 'status', {'status': 'next'})
		print 'result', result

	def youtube(text):
		print 'sent request'
		requests.post("http://localhost:8080/voice", data={'artist': '', 'title': text})
		print 'request sent'

	intents['shutdown'] = shutdown
	intents['play_music'] = play_music
	intents['pause_music'] = pause_music
	intents['back_music'] = back_music
	intents['next_music'] = next_music
	intents['youtube'] = youtube

	return intents

def test_wit():
	wit.init()
	# response = wit.text_query('play music', wit_access_token)
	response = wit.voice_query_auto(wit_access_token)
	print('Response: {}'.format(response))
	wit.close()

# test_wit()
setup_wit()
listen(create_intents())