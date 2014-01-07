import urllib
import smtplib
import sqlite3 as sqlite
from bs4 import BeautifulSoup
print 'MegaBus Ticket Checker v1.0\n'

mailSender = "account@gmail.com" #Gmail account being used to send email
mailSenderPassword = "accountpass" #Gmail account's password
cityCodes = {'Austin':320, 'austin':320, 'Dallas':317, 'dallas':317, 'Houston':318, 'houston':318} #Cities and their respective code

def city_error_check(city): #checks if city is in cityCodes (only required for user input, not SQL DB control)
	try:
		cityCodes[city]
		return city
	except KeyError:
		print "City misspelled or not in database.  Please try again."
		city = city_error_check(raw_input("Re-enter city: "))
	return city

def send_email(data, mailReceiver): #mailReceiver is email address of recipient
	print "Accessing Gmail servers to send email to {}".format(mailReceiver)
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

	print "Email sent to {}".format(mailReceiver)

def megabus_day_data(Month, Day, Year, destination, departure): #return trip details as list [departure, arrival, cost] for given parameters
	print "Accessing Megabus site for data"
	customURL = 'http://us.megabus.com/JourneyResults.aspx?originCode={}&destinationCode={}&outboundDepartureDate={}%2f{}%2f{}&inboundDepartureDate=&passengerCount=1&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundOtherDisabilityCount=0&inboundWheelchairSeated=0&inboundOtherDisabilityCount=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=&withReturn=0' .format(cityCodes[departure], cityCodes[destination], Month, Day, Year)

	dayData = BeautifulSoup(urllib.urlopen(customURL).read()).find_all("ul", class_="journey standard")

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
	return data

def config_data(instance): #return user details for instance given
	print "Accessing SQL Database for User {}".format(instance)
	configdb = sqlite.connect('config.db')
	with configdb:
		cursor = configdb.cursor()
		cursor.execute('SELECT * FROM users WHERE id=?', (instance,))
		return cursor.fetchone()

def config_to_day_data(instance):
	userDetails = config_data(instance)
	if userDetails == None:
		return None
	if not userDetails[8] == "yes":
		return "Inactive"
	return megabus_day_data(userDetails[5], userDetails[6], userDetails[7], userDetails[3], userDetails[4]), userDetails[2], userDetails[9]

#--------------------Start Main Program--------------------#

instance = 0

while True:
	instance = instance + 1
	instanceData = config_to_day_data(instance)
	if instanceData == None:
		print "User {} does not exist.".format(instance)
		print "Completed all user requests."
		break
	if instanceData == "Inactive":
		print "User with ID {} is inactive".format(instance)
		continue
	send_email(instanceData[0], instanceData[1])

