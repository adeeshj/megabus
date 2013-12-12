import urllib
import webbrowser
from bs4 import BeautifulSoup
print 'MegaBus Ticket Checker v0.2\n'


url = 'http://us.megabus.com/JourneyResults.aspx?originCode=317&destinationCode=320&outboundDepartureDate=1%2f12%2f2014&inboundDepartureDate=&passengerCount=1&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundOtherDisabilityCount=0&inboundWheelchairSeated=0&inboundOtherDisabilityCount=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=&withReturn=0'
data =  urllib.urlopen(url)
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
	departure = ""
	for string in tag.find("li", class_="two").p.stripped_strings:
		departure = departure + " " + string
	tempdata.append(departure[1:].encode('utf-8'))
	arrive = ""
	for string in tag.find("li", class_="two").find("p", class_="arrive").stripped_strings:
		arrive = arrive + " " + string
	tempdata.append(arrive[1:].encode('utf-8'))
	for string in tag.find("li", class_="five").p.stripped_strings:
		cost = string
	tempdata.append(cost.encode('utf-8'))	
	data.append(tempdata)

print 'The current trip details are:\n'

for each_trip in data:
	print each_trip[0]
	print each_trip[1]
	print "Cost: " + each_trip[2] + '\n'

webbrowser.open_new_tab(url)

	