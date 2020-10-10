#bot to keep track of how many and how often games are played on discord
#made by gurg
import discord
import sys
import logging
import time
import re
from config.config import TOKEN 
from user import *
from database_stuff.update_database import update_database
from generate_output import generate_output

logging.basicConfig(level=logging.INFO)#logs errors and debug info


#TODO
#implement sql stuff[x]
#implement commands to actually use the bot[x]
#Add functionality to allow people to pm the bot and get thier own personal gametimes[]
#Add commands so people can query gametimes about specific games[]
#get a better name[x]
#get a profile pic[]
#changed it so it displays the start and stop messages in different colours[x]
#implent a way to gradually add times to db(say every 10 mins)[]


#global variables-------------------------------------------
current_playing = [] # 
current_users = [] # list of just the users, makes it easy to check if they are playing something already


if TOKEN ==  "":
    print ("TOKEN not found, please add it in the config.py file.")
    sys.exit(0)

#given a tuple of activities the function will return the relevant Game object if the 
#   user is playing a game and return nothing otherwise
def find_game(activities):

    # if the activities is a tuple check all the elements to work out if one of them is a game
    if (isinstance(activities, tuple)):
        for i in range(len(activities)):
            if isinstance(activities[i], discord.Game):
                return activities[i]

        #if a game cant be found return false
        return None

    # if its not a tuple still check it
    elif isinstance(activities, discord.Game):
        return activities

    return None




client = discord.Client()

@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(activity=discord.Game(name="Selling your data..."))


@client.event
async def on_message(message):
    

    if message.author.id == client.user.id: # dont trigger on own messages, redundant? yeah but i cba testing
        return

    
    if message.content == "test":

        output = isinstance(message.author.activities[0], discord.Game)

        await message.channel.send(output)

    if message.content == "test-fg":

        print(find_game(message.author.activities))

#write a function that updates the database with info 
    


@client.event
async def on_member_update(before, after):
    c_time = time.strftime("%H:%M:%S") #current time

    b_game = find_game(before.activities)
    a_game = find_game(after.activities)
    
    print ("BEFORE: "+ str(b_game))
    print ("AFTER: "+ str(a_game))

client.run(TOKEN)




    
    
