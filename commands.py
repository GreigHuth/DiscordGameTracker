# code to handle the different commands given to the bot
import sqlite3
import datetime
from operator import itemgetter

#TODO


def top_games(limit):
    month = datetime.datetime.now().strftime("%B").upper()

    conn = sqlite3.connect("gametime.db")
    cursor = conn.execute('select * from ' + month) # gets all the columns from the db
    
    games = [game[0] for game in cursor.description] # list comprehension that puts all the column names into a list
    games.pop(0)

    # need to hard code to remove spotify
    games.remove("Spotify")

    totals = [0]*len(games)
    for i in range(len(games)): # puts all the totals in a  list
        
       cursor = conn.execute('select sum('+games[i]+') from '+month)
       totals[i] = cursor.fetchone()[0]# converts total to int
        

    totals = map(lambda x: x/3600, totals) # converts all the totals to hours

    game_totals = list(zip(games,totals)) #zips totals with the games then turns it back into a list because it works

    game_totals = sorted(game_totals,key=itemgetter(1), reverse = True) # sorts the list in descending order

    message = "Top %d games played in %s:\n```" % (limit, month.lower())

    if limit > 0:
        game_totals = game_totals[:limit] # only displays the number of games desired

        for game in game_totals:
            message += '%s - {0:.2f} hours\n\n'.format(game[1]) % game[0]

    else:   
        game_totals = game_totals[70]
        
        for game in game_totals:
            message += '%s-{0:.2f} hours\n'.format(game[1]) % game[0]

    message += '```'

    
    return message
