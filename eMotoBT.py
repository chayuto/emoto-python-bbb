#!/usr/bin/python
import threading,time
import Adafruit_BBIO.UART as UART
import serial
 


class readThread(threading.Thread):
    def __init__(self, threadID ,serial):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.serial = serial
    def run(self):
        print "Starting Read Thread..." + str(self.threadID)
        read_serial(self.serial)

# Define a function for the thread
def read_serial(serial):
	print "serial Read thread started"
	while True:
		try:
			print "reading..."
			data  = serial.read(1)
			
			
		except Exception, e:
			raise

class writeThread(threading.Thread):
    def __init__(self, threadID ,serial):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.serial = serial
    def run(self):
        print "Starting Write Thread..." + str(self.threadID)
        write_serial(self.serial)

# Define a function for the thread
def write_serial(serial):
	print "serial write thread started"
	for i in range(1,400):
		try:

			serial.write("attemp: " + str(i) +"." )
			time.sleep(0.5) 
			
		except Exception, e:
			raise

def BTInit():
	UART.setup("UART2")
	 
	ser = serial.Serial(port = "/dev/ttyO2", baudrate=9600)
	ser.close()
	ser.open()
	if ser.isOpen():
		print "Serial is open!"
		# Create two threads as follows
		try:
			# Create new threads
			thread1 = readThread(1, ser)
			thread2 = writeThread(2,ser)
			# Start new Threads
			thread1.start()
			thread2.start()


		except Exception, e:
			print e
			print "Error: unable to start thread"


	



#ser.close()


   





