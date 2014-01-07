import sqlite3 as sqlite

configdb = sqlite.connect('config.db')

with configdb:
	cursor = configdb.cursor()
	cursor.execute("ALTER TABLE users ADD cost TEXT")

	