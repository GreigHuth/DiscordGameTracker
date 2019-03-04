import sqlite3
import datetime
from user import *
# all the functions that deal with the sql database will be in here

#TODO
#Write function to update the database with new timings[ ]
#Write code to update columns when a new game has been found[ ]
#Write code to update records when a new user is found[ ]
#Write code to make a new table when it becomes a new month[ ]
#Add code to create the database if there isnt one already[ ]
#
def update_gametime(user):
	#takes User class as input and uses that to update the corrensponding record in the database
	current_month = datetime.datetime.now().strftime("%B").upper()

	conn = sqlite3.connect("gametime.db") #connection to db

	cursor = conn.execute('select * from ' + current_month) # gets all the columns from the db
	games = [game[0] for game in cursor.description] # list comprehension that puts all the column names into a list

	cursor = conn.execute('select USER_ID from ' +current_month)# same as above but for users
	users = [user[0] for user in cursor.description] 

	if user.game in games and user.id in users :
		total = user.end - user.start





def add_new_game(user, conn, month): # takes user, db connection and current month as input
	conn.execute('alter table '+month+' add '+user.game+' text')


def add_new_user(user, conn, month):
	conn.execute('')

def make_new_table(user):
	pass

def init_database(user):
	pass

