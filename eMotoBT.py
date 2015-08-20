#!/usr/bin/python
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

exit_Flag = 0;
serial_Init_Flag = 0
ser = None;

threads = []

class readThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print "Starting Read Thread..." 

# Define a function for the thread
def read_serial():
	print "serial Read thread started"
	while (not exit_Flag) and serial_Init_Flag :
		try:
			print "reading..."
			data  = ser.read(1)
			if len(data) > 0:
				if ord(data) == PREAMBLE0:
					data  =  ser.read(1)
					if len(data) > 0:
						if ord(data) == PREAMBLE1:
							print 'preamble detected!'
							serial_Read_Header()
							
					else:
						print 'Error Len 0'
			else:
				print 'Error Len 0'

		except Exception, e:
			raise

def serial_Read_Header():
	header =  ser.read(6)
	if len(header) > 0:
		print 'Header:' + header.encode('hex')
		print 'trasaction ID:' + str(ord(header[0]))
		cmdID = ord(header[1])
		print str(cmdID)
		print 'size0:' + str(ord(header[2]))
		print 'size1:' + str(ord(header[3]))
		print 'headerCRC:' + str(ord(header[4]))
		print 'contentCRC:' + str(ord(header[5]))

		contentSize = ord(header[2])*256 + ord(header[3])

		contentBytes =  ser.read(6)
			if len(contentBytes) > 0:
				if cmdID == SET_COMMAND:
					analyse_SET_content_bytes(header,contentBytes);
				else if cmdID ==GET_COMMAND:

			else:
				print 'Error Len 0'
	else:
		print 'Error Len 0'

def varify_packet(headerBytes,contentBytes):
	return True

def analyse_SET_content_bytes(headerBytes,contentBytes):
	print '%X' % ord(contentBytes[0])
	pass

def analyse_GET_content_bytes(headerBytes,contentBytes):
	print '%X' % ord(contentBytes[0])
	pass

def send_ACK:
	pass


class writeThread(threading.Thread):
    def __init__(self,bytes):
        threading.Thread.__init__(self)
        self.bytes = bytes
    def run(self):
        print "Starting Write Thread..." 
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
	ser.timeout= 5
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



