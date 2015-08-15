#!/usr/bin/python
import urllib2
import json

def getAdsSchedule(token):
	url = 'https://emotovate.com/api/ads/all/'+token+'?deviceId=00000000&lat=null&lng=null';
	req = urllib2.Request(url)
	#req.add_header('Content-Type', 'application/json')

	response = urllib2.urlopen(req)

	data = response.read()

	scheduleListJson = json.loads(data)

	scheduleList = []
	for scheduleEntryJson in scheduleListJson:
		scheduleEntry = AdsScheduleEntry(scheduleEntryJson);
		scheduleList.append(scheduleEntry)

	return scheduleList

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




      
