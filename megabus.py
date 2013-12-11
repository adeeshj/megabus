import urllib
from bs4 import BeautifulSoup
print 'MegaBus Ticket Checker v0.1\n'

data =  urllib.urlopen('http://us.megabus.com/JourneyResults.aspx?originCode=317&destinationCode=320&outboundDepartureDate=1%2f12%2f2014&inboundDepartureDate=&passengerCount=1&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundOtherDisabilityCount=0&inboundWheelchairSeated=0&inboundOtherDisabilityCount=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=&withReturn=0')
#Using the date Jan 12, 2014 from Dallas to Austin.

webData = data.read()
soupData = BeautifulSoup(webData)

if 'No journeys have been found for the date selected' in webData:
	print "Megabus tickets not for sale yet."
else:
	print "Buy your Megabus tickets!"

dayData = soupData.body.form.find("div", id="wrapper").find("div", id="container").find("div", class_="mainContent").find("div", class_="cont_wraper").find("div", class_="cont_middlecurve").div.div.div.div.div.find("div", class_="journeyresult").find("div", class_="content").div.find_all("ul", class_="journey standard")

data = []

for tag in dayData:
	tempdata = []
	tempstring = ""
	for string in tag.find("li", class_="two").p.stripped_strings:
		tempstring = tempstring + " " + string
	tempdata.append(tempstring.encode('utf-8'))
	
	