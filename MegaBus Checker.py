import urllib

def settings():
	dataFile = open('data.txt', 'wb')
	dataFile.write('ExistingUser\n')
	for sting in ['Departure Location:', 'Arrival Location:', 'Departure Year:', 'Departure Month:', 'Departure Day:']:
		temp = str(input(sting)) + '\n'
		dataFile.write(temp)

#Create dictionary for locations
cityCodes = {'Austin':320, 'austin':320, 'Dallas':317, 'dallas':317, 'Houston':318, 'houston':318}

dataFile = open('data.txt', 'rb')
data = dataFile.readlines()
dataFile.close()

#Setup textual UI
print 'MegaBus Ticket Checker v0.1'

if data[0] == 'FirstTimeUser' or 'ExistingUser':
	print 'In order to use MegaBus checker, please fill in your criteria!'
	settings()
	dataFile = open('data.txt', 'rb')
	data = dataFile.readlines()

	dataFile.close()

print 'Type enter to check MegaBus availibility'

webscrape =  urllib.urlopen('http://us.megabus.com/JourneyResults.aspx?originCode={}&destinationCode={}&outboundDepartureDate={}%2f{}%2f{}&inboundDepartureDate=&passengerCount=1&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundOtherDisabilityCount=0&inboundWheelchairSeated=0&inboundOtherDisabilityCount=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=&withReturn=0'.format(cityCodes[data[1]], cityCodes[data[2]], data[4], data[5], data[3]))


if 'No journeys have been found for the date selected' in webscrape.read():
	print 'Megabus tickets to ' + data[2] + ' from ' + data[1] + ' not for sale yet.'
else:
	print "Buy your Megabus tickets!"
	

