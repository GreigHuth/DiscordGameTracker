import sqlite3
from discord.utils import find
import datetime
from operator import itemgetter

#prints a map object
def print_iterator(it):
    for x in it:
        print(x, end=' ')
    print('')



#command that lets people see thier own personal gametimes
def mygames(user_id, month):

    conn = sqlite3.connect("gametime.db")

    cursor = conn.execute('select * from ' +month+ ' where ID = ' +user_id) #gets all the times for the user who issued the command
    times = list(cursor.fetchall()[0]) # puts the times in a list and makes them integers
    times.pop(0) # removes 
    times =  map(lambda x: x/3600, times) # converts all the times from seconds to hours 
    

    cursor = conn.execute('select * from '+month) 
    games = [game[0] for game in cursor.description]#puts all the games played in the month in a list
    games.pop(0)


    game_totals = zip(games,times) 

    
    
    game_totals = [i for i in game_totals if i[0] != "Spotify" ]
    print_iterator(game_totals)
    game_totals = [i for i in game_totals if i[1] > 0] # removes all the zero entries
    game_totals = sorted(game_totals,key=itemgetter(1), reverse = True) # sorts the list in descending order


    #begin constructing message
    message = "Top games for YOU in %s:\n```" %(month.lower())
    
    for game, time  in game_totals:
        message += "%s - {0:.2f}hours \n".format(time) % game[0]

    message += '```'

    return message



