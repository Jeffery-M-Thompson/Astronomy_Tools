#!/usr/bin/env python

import csv
import MySQLdb
import sys
import getpass

user = raw_input('Enter Username: ')
passwd =  getpass.getpass('Enter Password: ')
mydb = sys.argv[1]
inputFile = sys.argv[2]

# Open database connection

db = MySQLdb.connect(host='localhost',
    user= user,
    passwd= passwd,
    db= mydb)
    
# prepare a cursor object using cursor() method

cursor = db.cursor()


columns = "ra, dec, l, b, psfMag_u, psfMag_g, psfMag_r, psfMag_i, psfMag_z,\
extinction_u, extinction_g, extinction_r, extinction_i, extinction_z"
csv_data = csv.reader(file(inputFile))
next(csv_data, None)
for row in csv_data:
	# Prepare SQL query to INSERT a record into the database.
	
	sql =	"INSERT INTO stars(\
			ra, declination, l, b, psfMag_u, psfMag_g, psfMag_r, psfMag_i, \
			psfMag_z, extinction_u, extinction_g, extinction_r, extinction_i, \
			extinction_z) \
			VALUES (\
			%s, %s, %s, %s, %s, %s, %s, %s, %s,\
			%s, %s, %s, %s, %s)" % tuple(row)
	try:
		# Execute the SQL command
		cursor.execute(sql)
		# Commit your changes in the database
		db.commit()
	except MySQLdb.Error, e:
		# Rollback in case there is any error
		try:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		except IndexError:
			print "MySQL Error: %s" % str(e)
		print row
		db.rollback()



# disconnect from server
db.close()


print "Done"
