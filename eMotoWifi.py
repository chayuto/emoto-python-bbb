#!/usr/bin/python
from wifi import Cell, Scheme

import subprocess

import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def connectToSavedWifi():
	
	print 'connecting to Wifi'

	'''
	scheme = Scheme.find('wlan0', 'eMoto')
	print scheme
	scheme.activate()
	'''
	subprocess.call(["sudo wifi connect eMoto"], shell=True)

	#get_ip_address('wlan0')  # '192.168.0.110'

def setupWifiScheme(SSID,key = None):

	cellToConnect = None
	# get all cells from the air
	for cell in Cell.all('wlan0'):
		
		if cell.ssid == SSID:
			print 'found target SSID'
			cellToConnect = cell

	print 'saving SSID config..'
	if cellToConnect != None:
		if key == None:
			scheme = Scheme.for_cell('wlan0','eMoto',cellToConnect)
		else:
			scheme = Scheme.for_cell('wlan0','eMoto',cellToConnect,key)
		try:
			scheme.save()
		except AssertionError:
			oldScheme = Scheme.find('wlan0', 'eMoto')
			oldScheme.delete()
			scheme.save()

	schemes = list(Scheme.all())

	print schemes

	








