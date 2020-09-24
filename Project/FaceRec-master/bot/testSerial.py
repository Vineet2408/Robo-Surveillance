import serial
import pyttsx3
import speech_recognition as sr
import time
from threading import *

e=pyttsx3.init('sapi5')
voices=e.getProperty('voices')
e.setProperty('voice',voices[0].id)


def takeCmd():
	r=sr.Recognizer()
	with sr.Microphone() as source:
		print('say')
		r.pause_threshold=0.5
		audio=r.listen(source)
		q='hello'
		try:
			q=r.recognize_google(audio,language='en-in')
			print(q)
			return q
		except Exception as e:
			print('not recognized')
			return 'error'
		return q

def speak(s):
	e.say(s)
	e.runAndWait()
	return 1
	
speak("hello i am Agent bot made by robo sparks")

def threadfun():
	while True:
		time.sleep(0.010)
		print('inside loop')
		q=takeCmd().lower()
		print('q=',q)
		
		if 'hello' in q:
			speak('hiighye')
			print(q)
		
		elif ('start motors' in q) or ('start motor' in q):
			v=speak('initiating motors')
			print(v)
		
		elif 'quit' in q:
			v=speak('i am programmed by  vineet ')
			print(v)
			v=speak('so i cannot quit coz he never quits')
			print(v)
			v=speak('say some thing but never quit')
			print(v)
			
		
		elif 'disconnect' in q:
			v=speak('disconnecting the server')
			print(q)
			break
			exit()
			break
		
if __name__=='__main__':
	t=Thread(target=threadfun)
	t.start()
	t.join()
	