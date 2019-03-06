import sqlite3
import datetime
import re
from user import *
# all the functions that deal with the sql database will be in here

#TODO
#Write function to update the database with new timings[x]
#Write code to update columns when a new game has been found[x]
#Write code to update records when a new user is found[x]
#Write code to make a new table when it becomes a new month[x]
#Add code to create the database if there isnt one already[x]

#global variables
month = datetime.datetime.now().strftime("%B").upper()

def update_database(user):
	#takes User class as input and uses that to update the corrensponding record in the database
	
	user_id = str(user.id)
	game = user.game
	game = re.sub(r'\W+','',game)
	print(game)
	
	while (True): #attempts to connect to db, if unsuccessful creates it then tries again
		try:
			conn = sqlite3.connect("gametime.db") #connection to db
			break;

		except: # if cant connect to db, make a new one
			print ("No gametime.db file detected, creating new one.")
			init_db(month) # initialises the db if one doesnt exist
		
	conn.execute('create table if not exists '+month+' (ID text PRIMARY KEY);' )# creates table for new month


	cursor = conn.execute('select * from ' + month) # gets all the columns from the db
	games = [game[0] for game in cursor.description] # list comprehension that puts all the column names into a list

	cursor = conn.execute('select ID from ' +month)# same as above but for users
	users = [i[0] for i in list(cursor)]

	if game not in games:
		add_new_game(game, conn, month) # adds new game if not already in db

	if user_id not in users:
		add_new_user(user_id, conn, month) # adds new user if not already in db

	playtime = round(user.end - user.start)#playtime to be added rounded to nearest int
	update_gametime(user_id, conn, month, playtime, game)#updates db with new gametime

	conn.close()

def update_gametime(user_id,conn,month, playtime, game):
	
	conn.execute('update '+month+' set '+game+'='+game+'+'+str(playtime)+' where ID=?',(user_id,))
	conn.commit()

def add_new_game(game, conn, month):
	conn.execute('alter table '+month+' add column '+game+' integer default 0')
	conn.commit()


def add_new_user(user_id, conn, month):
	conn.execute('insert into '+month+' (ID) values (?)', (user_id,))
	conn.commit()


def init_db(month): # initialises the db 
	f = open("gametime.db","w")
	f.close()
	conn = sqlite3.connect("gametime.db")
	conn.execute("create table "+month+"(ID text PRIMARY KEY);")
	conn.commit()
	conn.close()