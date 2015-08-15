#!/usr/bin/python
from eMotoAuthen import getToken,login 
from eMotoAds import getAdsSchedule,Ads,AdsScheduleEntry

from wand.image import Image
from wand.display import display

print "===================================="
print "  eMotoCell Script V0.0815.1636   "
print "===================================="

loginResponse = login('cGV0ZXIuYXlyZUBlbW90b3ZhdGUuY29tOnBhc3N3b3Jk');

print 'token:' + getToken();

print 'rethrieve Ads Schedule'

scheduleList =  getAdsSchedule(getToken());

imageURL = "" 
ads = None

for scheduleEntry in scheduleList: 
	print ''
	print 'From: ' + scheduleEntry.getFrom();
	print 'To: ' + scheduleEntry.getTo();

	adsList = scheduleEntry.getAdsList();

	for adsObj in adsList:

		print "    ID: "+adsObj.getID();
		print "    Description: "+adsObj.getDescription();
		print "    URL: "+adsObj.getUrl();
		imageURL =  adsObj.getUrl();
		ads =  adsObj;

imageData= ads.getAdsImageData()
with Image(file=imageData) as img:
	print('format =', img.format)
	print('size =', img.size);
	width = img.width
	height = img.height

'''
	display(img);
'''



