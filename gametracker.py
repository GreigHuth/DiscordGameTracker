# bot to keep track of how many and how often games are played on discord
# made by gurg
import re
import datetime
import time 
import sys
import sqlite3
import discord
import logging 
import asyncio

from generate_output import generate_output
from update_database import update_database
from user import User


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
            self.conn = sqlite3.connect("file:gt"+datetime.datetime.now().strftime("%Y")+".db?mode=rw", uri=True) #connection to db
        except:
            sys.exit("No database file detected, make a file called gt<current year>.db")

        print("Database connection successful!")

        #scrape all the users to see if they are already playing games, if they are, start tracking them
        print("Scanning server for gamers...")
        for guild in self.guilds:
            for member in guild.members:
                game = find_game(member.activities)
                if game :
                    user = User(member.id, game, time.time())
                    print("%s is playing %s" % (user.id, user.game))
                    await self.add_user(user)


        print("The bot is ready!")
        await self.change_presence(activity=discord.Game(name="Selling your data..."))


    # coroutine that runs whenever a message is sent to any channel in the server
    # message - class representing the message sent, contains details about the author, channel, etc 

    async def on_message(self, message):

        if message.author.id == self.user.id:  # dont trigger on own messages, redundant? yeah but i cba testing
            return

        #only do stuff if the message is actually a command
        if message.content.split()[0] in self.COMMANDS :
            output = generate_output(message)
            await message.channel.send(output)



    # coroutine that runs whenever a member updates thier activity status game or customs status
    # before -  the state of the user before the update
    # after  -  the state of the user after the update 
    async def on_member_update(self, before, after):

        if after.bot == True:  # if the user is a bot ignore it
            return


        # check to see if user if user is in list of current players
        #   if they are then check to see if they stopped playing a game and if they did then remove them from the list of people playing games 
        #   else do nothing
        #   
        # else record the time and create a class for the user and then add the user to the list of current players 

        game = find_game(after.activities)
        user = User(after.id, game, int(time.time()))
        

        #first check to see if they are playing a game now
        if game:
            if after.id not in self.currently_playing:
                #if the are playing a game and werent before then start tracking them
                await self.add_user(user)
                

        #if they arent playing a game then check if they were
        else:
            if after.id in self.currently_playing:
                await self.remove_user(user)
                
        

    #function to run and update the database every second?
    async def update_times(self):

        #for id, user in currently_playing:

           #calculate how long they have been playing for 
           # update the database with the new value 
           #update_database(user, self.conn)

        await self.wait_until_ready()
        while not self.is_closed():
            #update_database(self.currently_playing, self.conn)
            await self.test()
            await asyncio.sleep(5)

        return


    async def test(self):
        print("test")

    #add user to list of tracker players
    async def add_user(self, user):
        #NOTE: RACE CONDITION PROBABLY 
       
        print("%s started playing %s" % (user.id, user.game))
        self.currently_playing[user.id] = user


    #remove user from list of tracker players
    async def remove_user(self, user):
        #if they were then remove them from the list so the database stops tracking them
        print("%s stopped playing %s" % (user.id, user.game))
        self.currently_playing.pop(user.id)

    

