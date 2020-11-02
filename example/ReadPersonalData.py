from smartcard.System import readers
from libts import TSCns



if __name__ == "__main__":
	r = readers()
	reader = r[0]
	connection = reader.createConnection()
	connection.connect()
	tscns = TSCns(connection)	

	print("Full Name: {} {}".format(tscns.NETLINKFormatGetName(),tscns.NETLINKFormatGetSurname()))
	print("Birth: {}".format(tscns.NETLINKFormatGetDateOfBirth()))
	print("Cf: {} ".format(tscns.NETLINKFormatGetCf()))
	print("Start - End Validity: {} - {}".format(tscns.NETLINKFormatGetTsStartValidity(),tscns.NETLINKFormatGetTsEndValidity()))
	print("Residence Address: {}".format(tscns.NETLINKFormatGetAddress()))

