import sqlite3
from discord.utils import find
import discord
import datetime
from config.config import EMBED_COLOUR, EMBED_URL
from operator import itemgetter


#command that lets people see thier own personal gametimes
def mygames(user_id, month, conn):


    cursor = conn.execute('select * from ' +month+ ' where ID = ' +user_id) #gets all the times for the user who issued the command
    times = list(cursor.fetchall()[0]) # puts the times in a list and makes them integers
    times.pop(0) # removes ID
    times =  map(lambda x: x/3600, times) # converts all the times from seconds to hours 
    

    cursor = conn.execute('select * from '+month) 
    games = [game[0] for game in cursor.description]#puts all the games played in the month in a list
    games.pop(0)# removes ID


    game_totals = zip(games,times) 
    game_totals = [i for i in game_totals if i[0] != "Spotify" ] # removes spotify
    game_totals = [i for i in game_totals if i[1] > 0] # removes all the zero entries
    game_totals = sorted(game_totals,key=itemgetter(1), reverse = True) # sorts the list in descending order

    #begin constructing message
    title = "Top 10 games youve played in %s:\n" %(month.lower()) 
    i = 1
    content = ""
    for game, time  in game_totals:
        content += "%d: %s - {0:.2f}hours \n\n".format(time) % (i,game)
        i += 1
    
    message = discord.Embed(title=title, type="rich", description=content, colour=EMBED_COLOUR)
    

    return message



