from datetime import datetime
from discord.utils import find
from operator import itemgetter
from config.config import EMBED_COLOUR, EMBED_URL


import math
import sqlite3
import discord
import math

from .Command import Command


class topusers(Command):

    def __init__(self, conn, game_filter):
        super().__init__(conn, game_filter)

    def execute(self, args):
        # command that displays the top users of the given month in terms of game time

        channel = args[0]

        conn = self.conn
        month = datetime.now().strftime("%B").upper()
        
        cursor = conn.execute('select ID from '+month) # get all user ids
        users = [user[0] for user in cursor.fetchall()]

        cursor = conn.execute('select * from '+month)
        games = [game[0] for game in cursor.description] #get list of games
        games.pop(0) 

        totals = [0]*len(users)
        
        # sums up the times for each user
        for i in range(len(users)): 
            for game in games:
                cursor = conn.execute('select '+game+' from '+month+' where ID = '+users[i])
                totals[i] += cursor.fetchone()[0] 
            
            
        totals = map(lambda x: x/3600, totals) # converts all the times into hours

        user_totals = zip(users,totals)
        user_totals = [i for i in user_totals if i[0] not in self.filter ] # apply filter
        user_totals = sorted(user_totals,key=itemgetter(1), reverse = True) # sorts the list in descending order

        
        title = "Top %s gamers in %s:\n" % ("10", month.lower())
    

        #begin constructing message
        i = 1
        content = ""
        for user_id, time in user_totals:
            name = self.get_name(user_id, channel.guild)
            if name == None:
                continue
            
            hours = math.floor(time)
            minutes = round((time - hours)*60)
            content += '{}: {} - {} hours {} minutes\n\n'.format(i, str(name), hours, minutes)   
            i += 1

            if i > 10:
                break
        
        message = discord.Embed(title=title, type="rich", description=content, colour=EMBED_COLOUR)

        return message


    def get_name(self, id, guild):
        for member in guild.members:
            if str(id) == str(member.id):
                return member.name
