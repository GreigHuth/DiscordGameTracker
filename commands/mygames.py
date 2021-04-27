from datetime import datetime
from discord.utils import find
from operator import itemgetter

import math
import sqlite3
import discord
import math


from .Command import Command


class mygames(Command):

    def __init__(self, conn, game_filter):
        super().__init__(conn, game_filter)

    #command that lets people see thier own personal gametimes
    def execute(self, args):

        uid =  args[0]

        month = datetime.now().strftime("%B").upper()

        cursor = self.conn.execute('select * from {} where ID = {}'.format(month, str(uid))) #gets all the times for the user who issued the command
        times = list(cursor.fetchall()[0]) # puts the times in a list and makes them integers
        times.pop(0) # removes ID
        times =  map(lambda x: x/3600, times) # converts all the times from seconds to hours 
        

        cursor = self.conn.execute('select * from '+month) 
        games = [game[0] for game in cursor.description]#puts all the games played in the month in a list
        games.pop(0)# removes ID


        game_totals = zip(games,times) 
        game_totals = [i for i in game_totals if i[0] not in self.filter] # removes games in filter
        game_totals = [i for i in game_totals if i[1] > 0] # removes all the zero entries
        game_totals = sorted(game_totals,key=itemgetter(1), reverse = True) # sorts the list in descending order

        #begin constructing message
        title = "Top 10 games youve played in %s:\n" %(month.lower()) 
        
        body = self.construct_response(game_totals)

        message = discord.Embed(title=title, type="rich", description=body, colour=self.embed_colour)

        

        return message



