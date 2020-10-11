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

#NOTE: month being called all the time looks messy but its necessary so the bot doesnt need to be restarted all the time

def update_database(user):
	now = datetime.datetime.now()
	month = now.strftime("%B").upper()
	year = now.strftime("%Y")

	#takes User class as input and uses that to update the corrensponding record in the database
	game = user.game
	game = re.sub(r'\W+','',game)
	
	while (True): #attempts to connect to db, if unsuccessful creates it then tries again
		try:
			conn = sqlite3.connect("gt2020.db") #connection to db
			break

		except: # if cant connect to db, make a new one
			print ("No database file detected, creating new one.")
			init_db(month) # initialises the db if one doesnt exist


	c = conn.cursor()

	c.execute('create table if not exists '+month+' (ID text PRIMARY KEY);' )# creates table for new month


	 # gets all the columns from the db
	games = [game[0] for game in c.execute('select * from ' +month)] # list comprehension that puts all the column names into a list

	# same as above but for users
	users = [i[0] for i in list(c.execute('select ID from ' +month))]

	if game not in games:
		add_game(game, c) # adds new game if not already in db

	if user.id not in users:
		add_user(user.id, c, month) # adds new user if not already in db

	playtime = round(user.end - user.start)#playtime to be added rounded to nearest int
	update_gametime(user.id, c, playtime, game)#updates db with new gametime

	conn.close()



def update_gametime(user_id,c, playtime, game):

	month = datetime.datetime.now.strftime("%B").upper()
	
	c.execute('update '+month+' set '+game+'='+game+'+'+str(playtime)+' where ID=?',(user_id,))
	c.commit()

def add_game(game, c):	

	month = datetime.datetime.strftime("%B").upper()

	c.execute('alter table '+month+' add column '+game+' integer default 0')
	c.commit()


def add_user(user_id, c, month):
	c.execute('insert into '+month+' (ID) values (?)', (user_id,))
	c.commit()


def init_db(month): # initialises the db 
	f = open("gametime.db","w")
	f.close()
	conn = sqlite3.connect("gametime.db")
	conn.execute("create table "+month+"(ID text PRIMARY KEY);")
	conn.commit()
	conn.close()