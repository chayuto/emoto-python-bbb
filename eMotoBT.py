#!/usr/bin/python
import threading,time
import Adafruit_BBIO.UART as UART
import serial
 
#Flags
PREAMBLE0 = 0xEC;
PREAMBLE1 = 0xDF;

exit_Flag = 0;

threads = []

class readThread(threading.Thread):
    def __init__(self, threadID ,serial):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.serial = serial
    def run(self):
        print "Starting Read Thread..." + str(self.threadID)
        read_serial(self.serial)



class writeThread(threading.Thread):
    def __init__(self, threadID ,serial):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.serial = serial
    def run(self):
        print "Starting Write Thread..." + str(self.threadID)
        write_serial(self.serial)

# Define a function for the thread
def read_serial(serial):

	print "serial Read thread started"
	while not exit_Flag:
		try:
			print "reading..."
			data  = serial.read(1)
			if data == PREAMBLE0:
				data  = serial.read(1)
				if data == PREAMBLE1:
					print 'preamble detected!'

		except Exception, e:
			raise


# Define a function for the thread
def write_serial(serial):
	print "serial write thread started"
	i = 0 
	while not exit_Flag:
		try:
			time.sleep(0.5) 
			serial.write("attemp: " + str(i) +"." )
			i = i + 1 
			
		except Exception, e:
			raise

def BT_init():

	exit_Flag = 0;

	UART.setup("UART2")
	 
	ser = serial.Serial(port = "/dev/ttyO2", baudrate=9600)
	ser.timeout= 5
	ser.close()
	ser.open()
	if ser.isOpen():
		print "Serial is open!"
		# Create two threads as follows
		try:
			# Create new threads
			thread1 = readThread(1, ser)
			threads.append(thread1);
			thread2 = writeThread(2,ser)
			threads.append(thread2);
			# Start new Threads
			thread1.start()
			thread2.start()


		except Exception, e:
			print e
			print "Error: unable to start thread"

def BT_close():
	global exit_Flag
	exit_Flag = 1

	# Wait for all threads to complete
	for t in threads:
		t.join()

	print 'BT Threads closed'

#ser.close()


   





