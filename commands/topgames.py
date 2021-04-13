# code for the topgames command, returns the top games played with respect to certain parameters
import datetime
import sqlite3
from operator import itemgetter
import discord
from config.config import EMBED_COLOUR, EMBED_URL
import math

def topgames(month, conn): 
    #invoked when topgames command is typed into discord
    #queries the sqlite data base "gametime.db" and gets the total of the time each game has been played 
    #   in that month across all users


   cursor = conn.execute('select * from ' + month) 
   games = [game[0] for game in cursor.description] # list comprehension that puts all the column names into a list
   games.pop(0) # first column in the db are the IDs so it removes them

   totals = [0]*len(games)
   for i in range(len(games)): # puts all the totals in a  list  

      cursor = conn.execute('select sum('+games[i]+') from '+month)
      totals[i] = cursor.fetchone()[0]# converts total to int  

   totals = map(lambda x: x/3600, totals) # converts all the totals to hours


   game_totals = zip(games,totals) #zips totals with the games then turns it back into a list because it works
   game_totals = [i for i in game_totals if i[0] != "Spotify" ]# remove spotify
   game_totals = sorted(game_totals,key=itemgetter(1), reverse = True) # sorts the list in descending order

   title= "Top %s games played in %s:\n" % ("10", month.lower())

   #begin constructing message
   i = 1
   content = ""
   for game, time in game_totals:
      hours = math.floor(time)
      minutes = round((time - hours)*60)
      content += '{}: {} - {} hours {} minutes\n\n'.format(i, game, hours, minutes)
      i += 1

      if i > 10:
         break

    
   message = discord.Embed(title=title, type="rich", description=content, colour=EMBED_COLOUR)


    
   return message
