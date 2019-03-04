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

def update_database(user):
	#takes User class as input and uses that to update the corrensponding record in the database
	month = datetime.datetime.now().strftime("%B").upper()
	user_id = str(user.id)
	game= user.game.replace(" ","")
	'''
	while (True) #attempts to connect to db, if unsuccessful creates it then tries again
		try:
			conn = sqlite3.connect("gametime.db") #connection to db
			print("Connected to gametime.db!")
			break;

		except: # if cant connect to db, make a new one
			print ("No gametime.db file detected, creating new one.")
			f = open("gametime.db","w")
			f.close()
	'''
	cursor = conn.execute('select * from ' + month) # gets all the columns from the db
	games = [game[0] for game in cursor.description] # list comprehension that puts all the column names into a list

	cursor = conn.execute('select USER_ID from ' +month)# same as above but for users
	users = [i[0] for i in list(cursor)]

	if game not in games:
		add_new_game(game, conn, month) # adds new game if not already in db

	if user_id not in users:
		add_new_user(user_id, conn, month) # adds new user if not already in db

	playtime = user.end - user.start
	update_gametime(user_id, conn, month, playtime, game)#updates db with new gametime


def update_gametime(user_id,conn,month, playtime, game):
	print("Gametime updated!")
	conn.execute('update '+month+' set '+game+'='+game+'+'+str(playtime)+' where USER_ID=?',(user_id,))
	conn.commit()

def add_new_game(game, conn, month):
	conn.execute('alter table '+month+' add column '+game+' integer')
	conn.commit()


def add_new_user(user_id, conn, month):
	conn.execute('insert into '+month+' (USER_ID) values (?)', (user_id,))
	conn.commit()


def make_new_table(user):
	pass

	

