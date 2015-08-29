#!/usr/bin/python
import threading
from eMotoAuthen import getToken,login 
from eMotoAds import getAdsSchedule,Ads,AdsScheduleEntry
import eMotoBT 
import eMotoWifi
import time

#from wand.image import Image
#from wand.display import display

def loginSucessCallback():
	print 'token:' + getToken();

	print 'rethrieve Ads Schedule'

	getAdsSchedule(getToken(),getAdsScheduleCallBack);
	pass

def loginFailCallback():
	pass

def getAdsScheduleCallBack(scheduleList):

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
		'''
		with Image(file=imageData) as img:
			print('format =', img.format)
			print('size =', img.size);
			width = img.width
			height = img.height
			#display(img);
			time.sleep(5.5)
		'''
	print threading.activeCount()

while True:
	
	print "===================================="
	print "  eMotoCell Script V0.0829.1433"
	print "===================================="

	print '1) Testing BT functionality'
	print '2) Testing Wifi functionality'
	print '3) Testing Server functionality'
	print '0) Exit'
	
	try:
		choice = eval(raw_input('Choose functionality to run:'))

		if choice == 1:
			print 'Testing BT functionality...'
			eMotoBT.BT_init();
			keypress = raw_input('Press enter to continue...')
			eMotoBT.BT_close();

		elif choice == 2:
			print 'Testing Wifi functionality...'
			eMotoWifi.setupWifiScheme('OneForAll','@AwesomeHumbleAbode');
			eMotoWifi.connectToSavedWifi();

		elif choice == 3:
			print 'Testing Server functionality...'
			login('cGV0ZXIuYXlyZUBlbW90b3ZhdGUuY29tOnBhc3N3b3Jk',loginSucessCallback,loginFailCallback);

		elif choice == 0:
			exit();

		else:
			print 'invalid choice'

	except Exception:
		pass




	




