import urllib
import webbrowser
import smtplib
from bs4 import BeautifulSoup
print 'MegaBus Ticket Checker v0.8\n'

mailSender = "" #Gmail account being used to send email
mailSenderPassword = "" #Gmail account's password
mailReceiver = "" #Recipient of email


def url_customization(): #returns string of url
	departureDateMonth = input("Enter the departure month (as a number): ")
	departureDateDay = input("Enter the departure day: ")
	departureDayYear = input("Enter the departure year: ")
	customURL = 'http://us.megabus.com/JourneyResults.aspx?originCode=317&destinationCode=320&outboundDepartureDate={}%2f{}%2f{}&inboundDepartureDate=&passengerCount=1&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundOtherDisabilityCount=0&inboundWheelchairSeated=0&inboundOtherDisabilityCount=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=&withReturn=0' .format(departureDateMonth, departureDateDay, departureDayYear)
	return customURL

def send_email(data):
	gmailserver = smtplib.SMTP("smtp.gmail.com", 587)
	gmailserver.ehlo()
	gmailserver.starttls()
	gmailserver.ehlo()
	gmailserver.login(mailSender, mailSenderPassword)

	header = "Megabus Trip Details"
	message = ""

	for each_trip in data:
		message = message + each_trip[0] + "\n" + each_trip[1] + "\n" + each_trip[2] + "\n\n"

	gmailserver.sendmail(mailSender, mailReceiver, header + "\n\n\n" + message)

	gmailserver.quit()

url = url_customization()

data =  urllib.urlopen(url)

webData = data.read()
soupData = BeautifulSoup(webData)

if 'No journeys have been found for the date selected' in webData:
	print "Megabus tickets not for sale yet."
else:
	print "Buy your Megabus tickets!"

dayData = soupData.find_all("ul", class_="journey standard")

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

#print 'The current trip details are:\n'
#
#for each_trip in data:
#	print each_trip[0]
#	print each_trip[1]
#	print "Cost: " + each_trip[2] + '\n'

send_email(data)

print "done"