#!/usr/bin/python


from Crc import  CrcRegister,CRC8_CCITT

#TODO: finish packet class

class Packet():

	def __init__(self,headerBytes,contentBytes):
		self.headerBytes = headerBytes
		self.contentBytes = contentBytes

	def getHeaderBytes(self):
		return self.headerBytes

	def getContentBytes(self):
		return self.contentBytes

	def getTxnID(self):
		return ord(self.headerBytes[2])

	def getCMDID(self):
		return ord(self.headerBytes[3])

	def getContentCRC(self):
		return ord(self.headerBytes[6])

	def getHeaderCRC(self):
		return ord(self.headerBytes[7])

	def computeContentCRC(self):
		pass

	#check if the headerCRC,conentCRC and contentLength match
	def isValid(self):
		pass

	def getDID(self):
		return ord(self.contentBytes[0])
		
