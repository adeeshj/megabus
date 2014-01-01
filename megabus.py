import urllib
import smtplib
from bs4 import BeautifulSoup
print 'MegaBus Ticket Checker v0.9\n'

mailSender = "emailaddress@gmail.com" #Gmail account being used to send email
mailSenderPassword = "emailpassword" #Gmail account's password
cityCodes = {'Austin':320, 'austin':320, 'Dallas':317, 'dallas':317, 'Houston':318, 'houston':318} #Cities and their respective code

def city_error_check(city):
	try:
		cityCodes[city]
		return city
	except KeyError:
		print "City misspelled or not in database.  Please try again."
		city = city_error_check(raw_input("Re-enter city: "))
	return city

def url_customization(): #returns string of url
	departureDateMonth = raw_input("Enter the departure month (as a number): ")
	departureDateDay = raw_input("Enter the departure day: ")
	departureDayYear = raw_input("Enter the departure year: ")
	departureCity = city_error_check(raw_input("Enter the departure city: "))	
	arrivalCity = city_error_check(raw_input("Enter the arrival city: "))

	customURL = 'http://us.megabus.com/JourneyResults.aspx?originCode={}&destinationCode={}&outboundDepartureDate={}%2f{}%2f{}&inboundDepartureDate=&passengerCount=1&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundOtherDisabilityCount=0&inboundWheelchairSeated=0&inboundOtherDisabilityCount=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=&withReturn=0' .format(cityCodes[departureCity], cityCodes[arrivalCity], departureDateMonth, departureDateDay, departureDayYear)
	return customURL

def send_email(data, mailReceiver): #mailReceiver is email address of recipient

	#login to gmail servers
	gmailserver = smtplib.SMTP("smtp.gmail.com", 587)
	gmailserver.ehlo()
	gmailserver.starttls()
	gmailserver.ehlo()
	gmailserver.login(mailSender, mailSenderPassword)

	#prepare message as a string
	header = "Megabus Trip Details"
	message = ""
	for each_trip in data:
		message = message + each_trip[0] + "\n" + each_trip[1] + "\n" + each_trip[2] + "\n\n"

	#send message and quit server
	gmailserver.sendmail(mailSender, mailReceiver, header + "\n\n\n" + message)
	gmailserver.quit()

#--------------------Start Main Program--------------------#

#prepare URL and open as object
dayData = BeautifulSoup(urllib.urlopen(url_customization()).read()).find_all("ul", class_="journey standard")

#extract all relavent information into list
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

send_email(data, "emailreceiver@something.com")
print "\nEmail sent."