from Crc import  CrcRegister,CRC8_CCITT


def getCRC8FromIntList(list):
	crc = CrcRegister(CRC8_CCITT)
	crc.takeList(list)
	CRCval = crc.getFinalValue()
	return CRCval
	
def getCRC8FromString(string):
	crc = CrcRegister(CRC8_CCITT)
	crc.takeString(string)
	CRCval = crc.getFinalValue()
	return CRCval