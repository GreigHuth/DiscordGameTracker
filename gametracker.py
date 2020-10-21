# bot to keep track of how many and how often games are played on discord
# made by gurg
import re
from datetime import datetime
import time 
import sys
import sqlite3
import discord
import logging 
import asyncio

from generate_output import generate_output
from user import User

#interval at which the update database script runs abd therefor how much the database should be updated with
INTERVAL = 1

#HELPER functions

#given a tuple of "activities" the function will return the relevant Game object if the 
#   user is playing a game and return nothing otherwise
#returns a string if the user is playing a game and None otherwise
def find_game(activities):
# if the activities is a tuple check all the elements to work out if one of them is a game

    if (isinstance(activities, tuple)):
        for i in range(len(activities)):
            #Sprint("activity", activities[i])
            if isinstance(activities[i], discord.Game):
                return re.sub(r'\W+','',str(activities[i]))
            if isinstance(activities[i], discord.Activity):
                return re.sub(r'\W+','',str(activities[i].name))

        #if a game cant be found return false
        return None

    # if its not a tuple still check it
    elif isinstance(activities, discord.Game):
        return re.sub(r'\W+','',str(activities))

    return None



class gametracker(discord.Client):


    COMMANDS = ["!topgames", "!topusers", "!help", "!mygames"]

    # dict <users id, class representing user>
    currently_playing = {}
    conn = None
    prev_time = 0


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
                if member.bot == True:
                    print("%s: is a bot" % member.name)
                
                else:
                    game = find_game(member.activities)
                    if game :
                        user = User(member.id, game)
                        print("%s is playing %s" % (user.id, user.game))
                        await self.add_user(user)

        print("scanning finished")
        print("The bot is ready!")


    # coroutine that runs whenever a message is sent to any channel in the server
    # message - class representing the message sent, contains details about the author, channel, etc 

    async def on_message(self, message):

        if message.author.id == self.user.id:  # dont trigger on own messages
            return


        #TODO: Commands need re-implemented
        #only do stuff if the message is actually a command
        if message.content.split()[0] in self.COMMANDS :
            output = generate_output(message, self.conn)
            await message.channel.send(output)



    # coroutine that runs whenever a member updates thier activity status game or customs status
    # before -  the state of the user before the update
    # after  -  the state of the user after the update 
    async def on_member_update(self, before, after):

        if after.bot == True or before.bot == True:  # if the user is a bot ignore it
            print(after.bot == True)
            pass

        game = find_game(after.activities)
        user = User(str(after.id), game)


        #first check to see if they are playing a game now, if they are now and they previously werent, add them to cp
        if not (game == None):
            
            #if the user is playing a different game than before then remove it and re-add it
            if (after.id in self.currently_playing) and self.currently_playing[after.id].game != find_game(after.activities):
                await self.remove_user(user)

                self.last_update = time.time()
                await self.add_user(user)

            if find_game(before.activities) == find_game(after.activities):
                pass
            
            else:
                print("%s started playing %s" % (user.id, user.game))
                user.last_update = time.time()
                await self.add_user(user)
        
            

                

        #if they arent playing a game then check if they were, if they were remove them from cp
        if game == None:
            if str(after.id) in self.currently_playing:
                print("%s stopped playing %s" % (user.id, user.game))
                await self.remove_user(user)
                
        

    #function to run and update the database every 5 seconds
    async def update_times(self):

        await self.wait_until_ready()
        while not self.is_closed():
            #print("updating database")

            #current month
            month = datetime.now().strftime("%B").upper()

            #if the database connection doesn't exist yet then ignore this task
            if self.conn:

                #iterate through list of current players and update the database accordingly
                c = self.conn
                for uid, user in self.currently_playing.items():
                    #print("Updating info for user %s"% uid)
                    
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

                    user.last_update = self.update_gametime(user, c, month)#updates db with new gametime
                

                c.commit()
                #print("database updated")
            
            else:
                print("no database connection, skipping.")
            await asyncio.sleep(INTERVAL)


    def update_gametime(self, user, c, month):
        game = user.game

        now = time.time()
        interval = now - user.last_update 
        print ("%f seconds since last update for user: %s" % (interval, user.id))
        
        #actually update the sql database
        c.execute('update '+month+' set '+game+'='+game+'+'+str(interval)+' where ID=?',(user.id,))
        c.commit()

        return now


    def add_game_db(self, game, c, month):	
        c.execute('alter table '+month+' add column '+game+' integer default 0')
        c.commit()


    def add_user_db(self, user_id, c, month):
        c.execute('insert into '+month+' (ID) values (?)', (user_id,))
        c.commit()


    #add user to list of tracked players, als returns the time they were added
    async def add_user(self, user):
        self.currently_playing[user.id] = user


    #remove user from list of tracker players
    async def remove_user(self, user):
        del self.currently_playing[user.id]

    

