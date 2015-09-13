import urllib
import smtplib
import time
import sqlite3 as sqlite
from bs4 import BeautifulSoup
print 'MegaBus Ticket Checker v1.0\n'

mailSender = "" #Gmail account being used to send email
mailSenderPassword = "" #Gmail account's password
cityCodes = { #Cities and their respective code
	'Austin':320, 
	'austin':320, 
	'Dallas':317, 
	'dallas':317, 
	'Houston':318, 
	'houston':318
} 
monthCodes = { #months and their respective number
	1:'January',
	2:'February',
	3:'March',
	4:'April',
	5:'May',
	6:'June',
	7:'July',
	8:'August',
	9:'September',
	10:'October',
	11:'November',
	12:'December',
}

def city_error_check(city): #checks if city is in cityCodes (only required for user input, not SQL DB control)
	try:
		cityCodes[city]
		return city
	except KeyError:
		print "City misspelled or not in database.  Please try again."
		city = city_error_check(raw_input("Re-enter city: "))
	return city

def send_email(data, message, mailReceiver): #mailReceiver is email address of recipient
	print "Accessing Gmail servers to send email to {}".format(mailReceiver)
	#login to gmail servers
	gmailserver = smtplib.SMTP("smtp.gmail.com", 587)
	gmailserver.ehlo()
	gmailserver.starttls()
	gmailserver.ehlo()
	gmailserver.login(mailSender, mailSenderPassword)

	#prepare message as a string
	header = "Megabus Trip Details for {} {}, {} from {} to {}".format(monthCodes[parameters[0]], parameters[1], parameters[2], parameters[4], parameters[3])
	for each_trip in data:
		message = message + "\n\n" + each_trip[0] + "\n" + each_trip[1] + "\n" + each_trip[2] 

	#send message and quit server
	gmailserver.sendmail(mailSender, mailReceiver, header + "\n\n\n" + message)
	gmailserver.quit()

	print "Email sent to {}\n".format(mailReceiver)

def megabus_day_data(Month, Day, Year, destination, departure): #return trip details as list [departure, arrival, cost] for given parameters
	global parameters 
	parameters = (Month, Day, Year, destination, departure)

	print "Accessing Megabus site for data"
	customURL = 'http://us.megabus.com/JourneyResults.aspx?originCode={}&destinationCode={}&outboundDepartureDate={}%2f{}%2f{}&inboundDepartureDate=&passengerCount=1&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundOtherDisabilityCount=0&inboundWheelchairSeated=0&inboundOtherDisabilityCount=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=&withReturn=0' .format(cityCodes[departure], cityCodes[destination], Month, Day, Year)

	if "No journeys have been found for the date selected" in urllib.urlopen(customURL).read():
		return False

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

def config_to_day_data(instance): #returns ([depart, arrive, cost], email, cost)
	userDetails = config_data(instance)
	if userDetails == None:
		return None
	if not userDetails[8] == "yes":
		return "Inactive"
	return megabus_day_data(userDetails[5], userDetails[6], userDetails[7], userDetails[3], userDetails[4]), userDetails[2], userDetails[9]

def save_cost_data(allData, instance):
	configdb = sqlite.connect('config.db')
	with configdb:
		cursor = configdb.cursor()
		cursor.execute('UPDATE users SET Cost=? WHERE Id=?', (cost_template(allData), instance))

def cost_template(allData):
	temp = "("
	for trip in allData:
		temp = temp + trip[2] + ","
	temp = temp + ")"
	return temp


#--------------------Start Main Program--------------------#

while True:
	instance = 0

	while True:
		instance = instance + 1
		instanceData = config_to_day_data(instance)
		if instanceData == None: #checks if user exists
			print "User {} does not exist.".format(instance)
			print "Completed all user requests.\n"
			break
		if instanceData == "Inactive": #checks if user is still active
			print "User with ID {} is inactive".format(instance)
			continue
		if not instanceData[0]:
			print "User {} request not for sale yet.\n".format(instance)
			continue
		if instanceData[2] == "0": #checks if user has previous cost data
			send_email(instanceData[0], "Welcome to Megabus Checker. Please make sure to unblock aj.test.python@gmail.com if you wish to receive emails from this service.", instanceData[1])
			save_cost_data(instanceData[0], instance)
		else:
			if instanceData[2] == cost_template(instanceData[0]):
				print "User {} cost information did not change.  Email not sent.\n".format(instance)
			else:
				print "User {} cost information changed.".format(instance)
				send_email(instanceData[0], "Ticket prices for your trip date have changed.  Here are the updated prices.", instanceData[1])
	print time.strftime('%c') + ": Standby mode.  Safe to edit SQL Database for next 3 hours."			
	time.sleep(10800)
