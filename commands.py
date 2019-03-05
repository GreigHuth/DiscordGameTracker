# code to handle the different commands given to the bot
import sqlite3
import datetime


def top_games():
	month = datetime.datetime.now().strftime("%B").upper()

	conn = sqlite3.connect("gametime.db")
	cursor = conn.execute('select * from ' + month) # gets all the columns from the db
	
	games = [game[0] for game in cursor.description] # list comprehension that puts all the column names into a list
	games.pop(0) # gets rid of ID column

	totals = []
	for i in range(len(games)):
		totals[i] = conn.execute('select sum('+games[i]+') from '+month)

	totals = map(lambda x: x/3600, totals) # converts all the totals to hours
	game_totals = zip(games,totals)

	game_totals = sorted(game_totals,key=itemgetter(1))

	game_totals = game_totals[:5] # only returns top 5
	message = "Top 5 games played in '+month' (in hours):\n``` "
	for game in game_totals:
		message += '%s - %s hours played\n' % (game[0], game[1])
