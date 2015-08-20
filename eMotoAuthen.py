#!/usr/bin/python
import threading
import urllib2
import json
import ssl

token = "hello"
storedCredential = ""
tokenIsValid = False

class asyncAuthenThread(threading.Thread):
	def __init__(self,callBackExternSuccess,callBackExternFail,url):
		threading.Thread.__init__(self)
		self.callBackExternSuccess = callBackExternSuccess
		self.callBackExternFail = callBackExternFail
		self.url = url
	def run(self):
		global token
		req = urllib2.Request(self.url)
		req.add_header('Content-Type', 'application/json')
		data = []

		try:
			'''
			ctx = ssl.create_default_context()
			ctx.check_hostname = False
			ctx.verify_mode = ssl.CERT_NONE
			'''

			response = urllib2.urlopen(req, json.dumps(data) ) #,context=ctx)

			data = response.read()
			jsonResponse =  json.loads(data)
			token = jsonResponse["token"]
			self.callBackExternSuccess()
			print "login Success"
		
		except:
			print "unexpected error:"
			self.callBackExternFail();
			raise
		


def login(credential,successCallBack,failureCallBack):
	global token,storedCredential
	storedCredential = credential
	url = 'https://emotovate.com/api/security/authenticate/' + credential ;
	thread = asyncAuthenThread(successCallBack,failureCallBack,url);
	thread.start()


def getToken(): 
	global token
	return token



