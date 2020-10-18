import sqlite3
import datetime
import time
import re
# all the functions that deal with the sql database will be in here

#TODO
#Write function to update the database with new timings[x]
#Write code to update columns when a new game has been found[x]
#Write code to update records when a new user is found[x]
#Write code to make a new table when it becomes a new month[x]
#Add code to create the database if there isnt one already[x]

#NOTE: month being called all the time looks messy but its necessary so the bot doesnt need to be restarted all the time

def update_database(cp, conn):
	now = datetime.datetime.now()
	month = now.strftime("%B").upper()
	year = now.strftime("%Y")

	
	for uid, user in cp:

		print(uid)
		game = user.game
	
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

		update_gametime(user, c)#updates db with new gametime

	print("database updated")



def update_gametime(user, c):
	print("updating database...")
	month = datetime.datetime.now.strftime("%B").upper()
	game = user.game
	playtime = time.time() - user.start
	c.execute('update '+month+' set '+game+'='+game+'+'+str(playtime)+' where ID=?',(user.id,))
	c.commit()

def add_game(game, c):	
	print("adding new game to database")
	month = datetime.datetime.strftime("%B").upper()

	c.execute('alter table '+month+' add column '+game+' integer default 0')
	c.commit()


def add_user(user_id, c, month):
	print("adding new user to database")
	c.execute('insert into '+month+' (ID) values (?)', (user_id,))
	c.commit()
