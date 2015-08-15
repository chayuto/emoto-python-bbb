#!/usr/bin/python
import urllib2
import json

token = "hello"
storedCredential = ""
tokenIsValid = False

def login(credential):
	global token,storedCredential
	storedCredential = credential
	url = 'https://emotovate.com/api/security/authenticate/' + credential ;
	req = urllib2.Request(url)
	req.add_header('Content-Type', 'application/json')
	data = []

	try:
		response = urllib2.urlopen(req, json.dumps(data))

		data = response.read()
		jsonResponse =  json.loads(data)
		token = jsonResponse["token"]
		#TODO if the login is failure 
	
	except:
		print "unexpected error:"
		raise

	return jsonResponse

def getToken(): 
	global token
	return token



