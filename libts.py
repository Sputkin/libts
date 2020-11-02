
from smartcard.util import *
import datetime

class TSCns():

	ADPU_SELECT_FILE = [0x00, 0xA4]                  # APDU SELECT FILE command iso7816-4
	ADPU_READ_BINARY = [0x00, 0xB0, 0x00, 0x00,0x00] # APDU READ_BINARY command iso7816-4

	#ADPU_P1_SELECT_BY_IDENTIFIER = [0x00]           # select EF, DF or MF by file identifier 
	ADPU_P1_SELECT_BY_ABSOLUTE_PATH = [0x08]         # select file by absolute path from MF # ADPU
	#ADPU_P1_SELECT_BY_RELATIVE_PATH = [0x09]        # select file by relative path from current DF

	def __init__(self,connection):
		self.connection = connection
		self.__selectFile()
		self.dati = self.__readFile()

	def NETLINKFormatGetName(self):
		name = self.__NETLINKGetFieldByGroup("A1","04")
		#print("Name: {}".format(toASCIIString(name)))
		return toASCIIString(name)

	def NETLINKFormatGetSurname(self):
		surname = self.__NETLINKGetFieldByGroup("A1","87")
		#print("Surname: {}".format(toASCIIString(surname)))
		return toASCIIString(surname)

	def NETLINKFormatGetDateOfBirth(self):
		date = self.__NETLINKGetFieldByGroup("A3","80")
		#print("Birth: {}".format(toASCIIString(date)))
		return toASCIIString(date)


	def NETLINKFormatGetPyDateOfBirth(self):
		date = self.__NETLINKGetFieldByGroup("A3","80")
		date = toASCIIString(date)
		
		year = int(date[:4])
		month = int(date[4:6])
		day = int(date[6:])
		
		date = datetime.datetime(year,month,day)

		return date

	def NETLINKFormatGetCf(self):
		dati = self.__NETLINKGetFieldByGroup("A0","31")
		toHex = toHexString(dati).split(" ")
		indexes = [index for index, value in enumerate(toHex) if value == "81"]
		offset = indexes[1]
		size = dati[offset+1]
		cf = dati[offset+2:offset+2+size]
		#print("Cf: {}".format(toASCIIString(cf)))
		return toASCIIString(cf)

	def NETLINKFormatGetTsStartValidity(self):
		startValidity = self.__NETLINKGetFieldByGroup("A8","80")
		#print("Card start validity: {}".format(toASCIIString(startValidity)))
		return toASCIIString(startValidity)

	def NETLINKFormatGetPyDateTsStartValidity(self):
		startValidity = self.__NETLINKGetFieldByGroup("A8","80")
		startValidity = toASCIIString(startValidity)
		
		year = int(startValidity[:4])
		month = int(startValidity[4:6])
		day = int(startValidity[6:])
		
		startValidity = datetime.datetime(year,month,day)

		return startValidity

	def NETLINKFormatGetTsEndValidity(self):
		endValidity = self.__NETLINKGetFieldByGroup("A8","81")
		#print("Card end validity: {}".format(toASCIIString(endValidity)))
		return toASCIIString(endValidity)

	def NETLINKFormatGetPyDateTsEndValidity(self):
		endValidity = self.__NETLINKGetFieldByGroup("A8","81")
		endValidity = toASCIIString(endValidity)
		
		year = int(endValidity[:4])
		month = int(endValidity[4:6])
		day = int(endValidity[6:])
		
		endValidity = datetime.datetime(year,month,day)

		return endValidity


	def NETLINKFormatGetAddress(self):
		address = self.__NETLINKGetFieldByGroups("A4",["A1","A0"],"04")
		#print("Residence address: {}".format(toASCIIString(address))) # toASCIIString
		return toASCIIString(address)


	def NETLINKFormatGetDoctor(self):
		doctor = self.__NETLINKGetFieldByGroups("A7",["31"],"80")
		#print("Doctor: {}".format(toASCIIString(doctor))) # toASCIIString
		return toASCIIString(doctor)

	def NETLINKFormatGetPostalCode(self):
		postalCode = self.__NETLINKGetFieldByGroups("A4",["31","A1"],"81")
		return toASCIIString(postalCode)

	def __NETLINKGetFieldByGroup(self,group,field_tag):
		toHex = toHexString(self.dati).split(" ")
		offset = toHex.index(group)
		size = self.dati[offset+1]
		dati = self.dati[offset+2:offset+2+size]

		toHex = toHexString(dati).split(" ")
		offset = toHex.index(field_tag)
		size = dati[offset+1]
		field = dati[offset+2:offset+2+size]
		return field

	def __NETLINKGetFieldByGroups(self,group,sub_groups,field_tag):
		toHex = toHexString(self.dati).split(" ")
		offset = toHex.index(group)
		size = self.dati[offset+1]
		dati = self.dati[offset+2:offset+2+size]

		for sub_group in sub_groups:
			toHex = toHexString(dati).split(" ")
			offset = toHex.index(sub_group)
			size = dati[offset+1]
			dati = dati[offset+2:offset+2+size]

		toHex = toHexString(dati).split(" ")
		offset = toHex.index(field_tag)
		size = dati[offset+1]
		field = dati[offset+2:offset+2+size]
		return field


	def __selectFile(self):
		ABSOLUTE_PATH = [0x06, 0xD0, 0x00, 0xD1, 0x00,0xD1, 0x01, 0x00]
		COMMAND = self.ADPU_SELECT_FILE+self.ADPU_P1_SELECT_BY_ABSOLUTE_PATH+[0x00]+ABSOLUTE_PATH
		#print("request: {}".format(toHexString(COMMAND)))
		data, sw1, sw2 =  self.connection.transmit(COMMAND)
		#print("response: {:02X} {:02X}".format(sw1,sw2))

	def __readFile(self):
		#print("request: {}".format(toHexString(self.ADPU_READ_BINARY)))
		data, sw1, sw2 =  self.connection.transmit(self.ADPU_READ_BINARY)
		#print("response: {:02X} {:02X}".format(sw1,sw2))
		return data



