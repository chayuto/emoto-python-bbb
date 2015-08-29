#!/usr/bin/python
from eMotoBTPacket import Packet 
from eMotoUtill import getCRC8FromIntList,getCRC8FromString
import threading,time
import Adafruit_BBIO.UART as UART
import serial
import struct
 
#Flags
PREAMBLE0 = 0xEC;
PREAMBLE1 = 0xDF;

GET_COMMAND = 0xA5;
SET_COMMAND = 0x4B;
ACK_COMMAND = 0x6B;
NACK_COMMAND = 0x8E;

DID_DEVICE_ID 	= 0x00;
DID_HW_VERSION	= 0x01;
DID_FW_VERSION 	= 0x02;
DID_PROTOCOL 	= 0x03;
DID_C_TIME 		= 0x10;
DID_IMG_INFO	= 0x20;
DID_IMG_DATA 	= 0x21;
DID_IMG_ONLIST 	= 0x22;

DID_WIFI_SETUP = 0x30;
DID_AUTHEN_SETUP = 0x31;

exit_Flag = 0;
serial_Init_Flag = 0
ser = None;
serial_timeout = 2

threads = []

class readThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print "Starting Read Thread..." 
        read_serial()

# Define a function for the thread
def read_serial():
	print "serial Read thread started"
	while (not exit_Flag) and serial_Init_Flag :
		try:
			#print "reading..."
			data  = ser.read(1)
			if len(data) > 0:
				if ord(data) == PREAMBLE0:
					data  =  ser.read(1)
					if len(data) > 0:
						if ord(data) == PREAMBLE1:
							print 'preamble detected!'
							serial_Read_Header()
					else:
						#print 'Read Timeout'
						pass
			else:
				#print 'Read Timeout'
				pass

		except Exception, e:
			raise

def serial_Read_Header():
	header =  ser.read(6)
	if len(header) > 0:
		print 'Header:' + header.encode('hex')
		txnID = ord(header[0])
		print 'trasaction ID:' + str(txnID)
		cmdID = ord(header[1])
		print 'CMD ID:'+ str(cmdID)
		print 'size0:%X' % ord(header[2])
		print 'size1:%X' % ord(header[3])
		print 'contentCRC:%X' % ord(header[4])
		print 'headerCRC:%X' % ord(header[5])

		contentSize = ord(header[3]) * 256 + ord(header[2])

		print 'contentSize:' + str(contentSize)

		headerList = [PREAMBLE0, PREAMBLE1]
		for i in range(0,5):
			headerList.append(ord(header[i]))

		print headerList
		print 'Computed CRC: %X' % getCRC8FromIntList(headerList)

		contentBytes =  ser.read(contentSize)
		if len(contentBytes) > 0:

			mPacket = Packet(header,contentBytes);

			print 'Contents:' + contentBytes.encode('hex')
			if cmdID == SET_COMMAND:
				analyse_SET_content(mPacket);
				

			elif cmdID ==GET_COMMAND:
				analyse_GET_content(mPacket);

		else:
			#print 'Read Timeout'
			pass
	else:
		#print 'Read Timeout'
		pass

def analyse_SET_content(packet):	
	
	did = packet.getDID()
	txnID = packet.getTxnID()

	print 'SET DID:%X' % did

	if did == DID_WIFI_SETUP :
		print "SET DID_WIFI_SETUP"

		contentBytes = packet.getContentBytes()
		SSID = contentBytes[1:20]
		sec = contentBytes[21]
		key = contentBytes[22:61]

		print "SSID: " + SSID
		print "Sec Type: " + str(ord(sec)) 
		print "Key: " + key

		#TODO: call wifimodule to store info in eMotoCell

		#sending ack to the phone
		send_ACK(txnID,[0x02,0x23,0x04])
		pass

	if did == DID_AUTHEN_SETUP:

		print "SET DID_AUTHEN_SETUP"
		contentBytes = packet.getContentBytes()
		print "Credential: " + contentBytes 

		#TODO: store credential in eMotoCell

		#sending ack to the phone
		send_ACK(txnID,[0x02,0x23,0x04])


	elif did == DID_IMG_ONLIST:
		print "SET DID_IMG_ONLIST"
		send_ACK(txnID,[0x02,0x23,0x04])
		pass
	elif did == DID_IMG_DATA:
		print "SET DID_IMG_DATA"
		send_ACK(txnID,[0x02,0x23,0x04])
		pass

	

def analyse_GET_content(packet):
	
	did = packet.getDID()
	txnID = packet.getTxnID()

	print 'GET DID:%X' % did

	if did == DID_DEVICE_ID:
		send_ACK(txnID,[DID_DEVICE_ID, 0x00,0x00,0x00,0x00])
		pass
	elif did == DID_PROTOCOL:
		send_ACK(txnID,[DID_PROTOCOL,0x00,0x00])
		pass
	elif did == DID_FW_VERSION:
		send_ACK(txnID,[DID_FW_VERSION,0x00,0x00])
		pass
	elif did == DID_HW_VERSION:
		send_ACK(txnID,[DID_HW_VERSION,0x00,0x00])
		pass



def send_ACK(txnID,content):

	print 'sending ACK:'
	contentSize = len(content)
	contentSize0 = contentSize%256
	contentSize1 = contentSize//256
	headerList = [PREAMBLE0, PREAMBLE1,txnID, ACK_COMMAND,contentSize0,contentSize1]
		
	#get content CRC
	contentCRC = getCRC8FromIntList(content)
	print 'Computed content CRC: %X' % contentCRC

	headerList.append(int(contentCRC))

	#get header CRC
	headerCRC = getCRC8FromIntList(headerList)
	print 'Computed header CRC: %X' % headerCRC

	#build payload
	headerList.append(int(headerCRC))
	payloadList = headerList + content 
	print payloadList

	print 'Sending:' +str(len(payloadList)) +' bytes'

	write_serial( ''.join([chr(i) for i in payloadList ]) ) ;

	pass

class writeThread(threading.Thread):
    def __init__(self,bytes):
        threading.Thread.__init__(self)
        self.bytes = bytes
    def run(self):
        #print "Starting Write Thread..." 
        ser.write(self.bytes)

# Define a function for the thread
def write_serial(bytes):
	if serial_Init_Flag:
		# Create two threads as follows
		try:
			thread2 = writeThread(bytes)
			threads.append(thread2);
			thread2.start()
			
		except Exception, e:
			print e
			print "Error: unable to write start thread"
	else:
		print "Serial is Closed!" 

def BT_init():

	global exit_Flag, serial_Init_Flag, ser

	exit_Flag = 0;

	UART.setup("UART2")
	 
	ser = serial.Serial(port = "/dev/ttyO2", baudrate=9600)
	ser.timeout= serial_timeout
	ser.close()
	ser.open()
	if ser.isOpen():

		serial_Init_Flag = 1;

		print "Serial is open!"
		try:
			# Create new threads
			thread1 = readThread()
			threads.append(thread1);
			# Start new Threads
			thread1.start()
			
		except Exception, e:
			print e
			print "Error: unable to start thread"

def BT_close():
	global exit_Flag,serial_Init_Flag 
	exit_Flag = 1

	# Wait for all threads to complete
	for t in threads:
		t.join()

	print 'BT Threads closed'

def BT_error_check():
	pass



