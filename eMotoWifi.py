#!/usr/bin/python
from wifi import Cell, Scheme
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
	scheme = Scheme.find('wlan0', 'eMoto')
	print scheme
	scheme.activate()
	get_ip_address('wlan0')  # '192.168.0.110'


cellToConnect = None
# get all cells from the air
for cell in Cell.all('wlan0'):
	print cell.ssid
	print cell.encryption_type
	if cell.ssid == '379':

		print 'found!'
		cellToConnect = cell

if cellToConnect != None:
	scheme = Scheme.for_cell('wlan0','eMoto',cellToConnect,'csek17l3')
	try:
		scheme.save()
	except AssertionError:
		oldScheme = Scheme.find('wlan0', 'eMoto')
		oldScheme.delete()
		scheme.save()

schemes = list(Scheme.all())

print schemes

connectToSavedWifi()




