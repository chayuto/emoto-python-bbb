#!/usr/bin/python
from eMotoAuthen import getToken,login 
from eMotoAds import getAdsSchedule,Ads,AdsScheduleEntry
import eMotoBT 
import time

from wand.image import Image
from wand.display import display

print "===================================="
print "  eMotoCell Script V0.0817.1325   "
print "===================================="

loginResponse = login('cGV0ZXIuYXlyZUBlbW90b3ZhdGUuY29tOnBhc3N3b3Jk');

print 'token:' + getToken();

print 'rethrieve Ads Schedule'

scheduleList =  getAdsSchedule(getToken());

allAdsList = []

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
		allAdsList.append(adsObj);
		
print 'start Display loop'
print 'size: ' + str(len(allAdsList))
for adsObj in allAdsList:

	imageData= adsObj.getAdsImageData()
	with Image(file=imageData) as img:
		print('format =', img.format)
		print('size =', img.size);
		width = img.width
		height = img.height
		display(img);
		time.sleep(5.5)

'''
print 'Server Testing Completed...'
print 'Starting BT Service Thread...'

eMotoBT.BTInit();
'''






	




