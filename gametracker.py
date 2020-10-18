# bot to keep track of how many and how often games are played on discord
# made by gurg
import re
from datetime import datetime
import sys
import sqlite3
import discord
import logging 
import asyncio

from generate_output import generate_output
from update_database import update_database
from user import User

#interval at which the update database script runs
INTERVAL = 1

#HELPER functions

#given a tuple of activities the function will return the relevant Game object if the 
#user is playing a game and return nothing otherwise
#returns a string if the user is playing a game and None otherwise
def find_game(activities):
# if the activities is a tuple check all the elements to work out if one of them is a game
    if (isinstance(activities, tuple)):
        for i in range(len(activities)):
            if isinstance(activities[i], discord.Game):
                return re.sub(r'\W+','',str(activities[i]))

        #if a game cant be found return false
        return None

    # if its not a tuple still check it
    elif isinstance(activities, discord.Game):
        return re.sub(r'\W+','',str(activities))

    return None



class gametracker(discord.Client):


    COMMANDS = ["!topgames", "!topusers", "!help", "!mygames"]
    currently_playing = {}
    conn = None


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

       

        #create the task and run it in the background
        self.bg_task = self.loop.create_task(self.update_times())


    async def on_ready(self):

         #attempt to connect to db, throw exception if cannot
        try:
            print("Connecting to database...")
            self.conn = sqlite3.connect("file:gt"+datetime.now().strftime("%Y")+".db?mode=rw", uri=True) #connection to db
        except:
            sys.exit("No database file detected, make a file called gt<current year>.db")

        print("Database connection successful!")

        #scrape all the users to see if they are already playing games, if they are, start tracking them
        print("Scanning server for gamers...")
        for guild in self.guilds:
            for member in guild.members:
                game = find_game(member.activities)
                if game :
                    user = User(member.id, game)
                    print("%s is playing %s" % (user.id, user.game))
                    await self.add_user(user)

        print("scanning finished")
        print("The bot is ready!")
        await self.change_presence(activity=discord.Game(name="Selling your data..."))


    # coroutine that runs whenever a message is sent to any channel in the server
    # message - class representing the message sent, contains details about the author, channel, etc 

    async def on_message(self, message):

        if message.author.id == self.user.id:  # dont trigger on own messages, redundant? yeah but i cba testing
            return


        #TODO: Commands need re-implemented
        #only do stuff if the message is actually a command
        #if message.content.split()[0] in self.COMMANDS :
        #    output = generate_output(message)
        #    await message.channel.send(output)



    # coroutine that runs whenever a member updates thier activity status game or customs status
    # before -  the state of the user before the update
    # after  -  the state of the user after the update 
    async def on_member_update(self, before, after):

        if after.bot == True:  # if the user is a bot ignore it
            return

        game = find_game(after.activities)
        user = User(str(after.id), game)
        
        print(game==None)
        #first check to see if they are playing a game now
        if not (game == None):
            if str(after.id) not in self.currently_playing:
                print("%s started playing %s" % (user.id, user.game))
                await self.add_user(user)
                

        #if they arent playing a game then check if they were
        if game == None:
            print(self.currently_playing)
            print(after.id)
            if str(after.id) in self.currently_playing:
                print("%s stopped playing %s" % (user.id, user.game))
                await self.remove_user(user)
                
        

    #function to run and update the database every 5 seconds
    async def update_times(self):

        await self.wait_until_ready()
        while not self.is_closed():
            print("updating database")

            #current month
            month = datetime.now().strftime("%B").upper()

            #if the database connection doesn't exist yet then ignore this task
            if self.conn:

                #iterate through list of current players and update the database accordingly
                c = self.conn
                for uid, user in self.currently_playing.items():
                    print("Updating info for user %s"% uid)
                    
                    c.execute('create table if not exists '+month+' (ID text PRIMARY KEY);' )# creates table for new month

                    # gets all the columns from the db
                    cursor = c.execute('select * from ' +month)
                    games = [game[0] for game in cursor.description] # list comprehension that puts all the column names into a list

                    # same as above but for users
                    cursor = c.execute('select ID from ' +month)
                    users = [i[0] for i in list(cursor)]

                    if user.game not in games:
                        print("%s game not found adding to database" % user.game)
                        self.add_game_db(user.game, c, month) # adds new game if not already in db

                    if user.id not in users:
                        print ("%s uid not found adding to database" % uid)
                        self.add_user_db(user.id, c, month) # adds new user if not already in db

                    self.update_gametime(user, c, month)#updates db with new gametime
                

                c.commit()
                print("database updated")
            
            else:
                print("no database connection, skipping.")
            await asyncio.sleep(INTERVAL)


    def update_gametime(self, user, c, month):
        game = user.game
        c.execute('update '+month+' set '+game+'='+game+'+'+str(INTERVAL)+' where ID=?',(user.id,))
        c.commit()

    def add_game_db(self, game, c, month):	
        c.execute('alter table '+month+' add column '+game+' integer default 0')
        c.commit()

    def add_user_db(self, user_id, c, month):
        c.execute('insert into '+month+' (ID) values (?)', (user_id,))
        c.commit()

    #add user to list of tracked players
    async def add_user(self, user):
        self.currently_playing[user.id] = user

    #remove user from list of tracker players
    async def remove_user(self, user):
        del self.currently_playing[user.id]

    

