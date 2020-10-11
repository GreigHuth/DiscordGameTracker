# bot to keep track of how many and how often games are played on discord
# made by gurg
import discord
import time
import re
from user import User
from update_database import update_database
from generate_output import generate_output


class gametracker(discord.Client):


    COMMANDS = ["!topgames", "!topusers", "!help", "!mygames"]
    currently_playing = {}


    
    async def on_ready(self):
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


        if before.bot == True:  # if the user is a bot ignore it
            return

        # check to see if user if user is in list of current players
        #   if they are then check to see if they stopped playing a game and if they did then remove them from the list of people playing games 
        #   else do nothing
        #   
        # else record the time and create a class for the user and then add the user to the list of current players 
        

    #function to run and update the database every second?
    async def update_db(self):
        return
