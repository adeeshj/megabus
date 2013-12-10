import urllib
print 'MegaBus Ticket Checker v0.1\n'

data =  urllib.urlopen('http://us.megabus.com/JourneyResults.aspx?originCode=317&destinationCode=320&outboundDepartureDate=1%2f5%2f2014&inboundDepartureDate=&passengerCount=1&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundOtherDisabilityCount=0&inboundWheelchairSeated=0&inboundOtherDisabilityCount=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=&withReturn=0')


if 'No journeys have been found for the date selected' in data.read():
	print "Megabus tickets not for sale yet."
else:
	print "Buy your Megabus tickets!"
	input()
