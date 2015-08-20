#!/usr/bin/python
import threading
import urllib2
import json
import ssl


def getAdsSchedule(token,callBackExtern):
	url = 'https://emotovate.com/api/ads/all/'+token+'?deviceId=00000000&lat=null&lng=null';
	thread1 = asyncThread(callBackExtern,dataToscheduleList,url)
	# Start new Threads
	thread1.start()
	

def dataToscheduleList(data,callBack):
	scheduleListJson = json.loads(data)

	scheduleList = []
	for scheduleEntryJson in scheduleListJson:
		scheduleEntry = AdsScheduleEntry(scheduleEntryJson);
		scheduleList.append(scheduleEntry)

	callBack(scheduleList);


class asyncThread(threading.Thread):
	def __init__(self,callBackExtern,callBackIntern,url):
		threading.Thread.__init__(self)
		self.callBackExtern = callBackExtern
		self.callBackIntern = callBackIntern
		self.url = url
	def run(self):
		ctx = ssl.create_default_context()
		ctx.check_hostname = False
		ctx.verify_mode = ssl.CERT_NONE
		req = urllib2.Request(self.url)
		#req.add_header('Content-Type', 'application/json')
		response = urllib2.urlopen(req,context=ctx)
		data = response.read()
		self.callBackIntern(data,self.callBackExtern)


class AdsScheduleEntry:

	def __init__(self, scheduleJSON):
		self.scheduleJSON = scheduleJSON
		self.From = scheduleJSON["From"]
		self.To = scheduleJSON["To"]

		adsList = []
		adsJsonList = scheduleJSON["Ads"];
		for ads in adsJsonList:
			adsObj = Ads(ads)
			adsList.append(adsObj)

		self.adsList = adsList

	def getFrom(self):
		return self.From;

	def getTo(self):
		return self.To;

	def getAdsList(self):
		return self.adsList


class Ads: 
	def __init__(self, adsJSON):
		self.adsJSON = adsJSON
		self.Id = adsJSON["Id"]
		self.Url = adsJSON["Url"]
		self.Description = adsJSON["Description"]
		self.Extension = adsJSON["Extension"]
	
	def getID(self):
		return self.Id;

	def getUrl(self):
		return self.Url

	def getDescription(self):
		return self.Description

	def getExtension(self):
		return self.Extension

	def getAdsImageData(self):
		return urllib2.urlopen(self.getUrl())

	#Description
	#Extension




      
