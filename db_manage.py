import sqlite3 as lite
import datetime
import json

db = lite.connect("config.db", detect_types=lite.PARSE_DECLTYPES)

with db:
	cur = db.cursor()
	#cur.execute("DROP TABLE userdata")
	#cur.execute("CREATE TABLE UserData(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE)")
	#cur.execute("CREATE TABLE Routes(datetime TIMESTAMP, departure TEXT, destination TEXT, users TEXT, active INT, cost TEXT)")

	name = raw_input("Name: ")
	email = raw_input("Email: ")

	# insert into userdata table
	try:
		cur.execute("INSERT INTO userdata (name, email) values (?, ?)", (name, email))
	except lite.IntegrityError:
		pass


	day = datetime.datetime.strptime(raw_input("Date (MM/DD/YYYY): "), "%m/%d/%Y")
	departure = raw_input("Departure: ")
	destination = raw_input("Destination: ")

	
	cur.execute("SELECT users FROM routes WHERE datetime=? AND departure=? AND destination=?", (day, departure, destination))
	users = cur.fetchone()
	print users
	if users:
		 users = json.loads(users)
		 if 

	# insert into routes table
	cur.execute("INSERT INTO routes values (?, ?, ?, ?, ?, ?)", (day,	# datetime
																 departure,
																 destination,
																 json.dumps([]),	# users json set
																 1,	# active
																 json.dumps([])))	# cost json list

	db.commit()



