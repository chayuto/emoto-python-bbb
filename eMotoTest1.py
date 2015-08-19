#!/usr/bin/python
from eMotoAuthen import getToken,login 
from eMotoAds import getAdsSchedule,Ads,AdsScheduleEntry
import eMotoBT 
import eMotoWifi
import time

from wand.image import Image
from wand.display import display

print "===================================="
print "  eMotoCell Script V0.0819.1522   "
print "===================================="

print 'Testing BT functionality...'

eMotoBT.BT_init();
for i in range (1,30):
	time.sleep(1)
	print str(30 - i) + '...'
eMotoBT.BT_close();
exit()


#eMotoWifi.setupWifiScheme('379','csek17l3');
eMotoWifi.connectToSavedWifi();

print 'Testing Server functionality...'
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
print 'List size: ' + str(len(allAdsList))
for adsObj in allAdsList:
	print 'Displaying: ' + adsObj.getID() 
	imageData= adsObj.getAdsImageData()
	with Image(file=imageData) as img:
		print('format =', img.format)
		print('size =', img.size);
		width = img.width
		height = img.height
		#display(img);
		time.sleep(5.5)









	




