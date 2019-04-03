#bot to keep track of how many and how often games are played on discord
#made by gurg
import discord
import sys
import logging
import time
import re
from config import *
from user import *
from update_database import *
from commands import * 

logging.basicConfig(level=logging.INFO)#logs errors and debug info


#TODO
#implement sql stuff[x]
#implement commands to actually use the bot[x]
#Add functionality to allow people to pm the bot and get thier own personal gametimes[]
#make the overall bot more presentable[]
#pitch to people[]
#get a better name[x]
#get a profile pic[]
#write some bloody documentation[x]
#neaten up the code[]
#changed it so it displays the start and stop messages in different colours[x]
#implent a way to gradually add times to db(say every 10 mins)[]


#global variables-------------------------------------------
current_playing = [] # 
current_users = [] # list of just the users, makes it easy to check if they are playing something already
months = []
for i in range(1,13):
    months.append(datetime.date(2008, i, 1).strftime('%B').lower())

if TOKEN ==  "":
    print ("TOKEN not found, please add it in the config.py file.")
    sys.exit(0)

    
client = discord.Client()

@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(game=discord.Game(name="Selling your data..."))


@client.event
async def on_message(message):

    if message.author.id == client.user.id: # dont trigger on own messages
        return

    regex = re.search("!topgames|help(\s)?.*(\s)?[a-z]*", message.content) # matches message to regex, if no match then ignore
    
    if regex == None :
        return

    split_message = message.content.split() # splits message into command and then parameters
    
    output = handle_input(split_message)

    await client.send_message(message.channel, output)


@client.event
async def on_member_update(before, after):
    c_time = time.strftime("%H:%M:%S") #current time

    if before.bot == True: # if the user is a bot ignore it
        return

    elif before.game == None and after.game != None and before.id not in current_users : 
        #checks to see if user has started playing a game and is not already playing one
        
        print ("\033[1;32;40m%s: user %s has started playing %s." % (c_time, before.name, after.game.name))
        #The thing at the start makes the text green

        id = before.id
        game = after.game.name 
        start = time.time()
        end = None

        current_users.append(id) # add id to list of people currently playing games
        user= User(id, game, start, end) #creates new user
        current_playing.append(user) # adds new user to list of people currently playing games
    

    elif after.game == None and before.game != None : # a user has just stopped playing a game

        end = time.time() 
        for user in current_playing:
            # find current user in list of users playing games

            if after.id == user.id and before.game.name == user.game: 

                user.end = end # time user stopped playing the game
                time_played = user.end - user.start # total time the game was played 
                user.end = end

                print ("\033[1;31;40m%s: user %s played %s for %d seconds." % (c_time,after.name, before.game.name, time_played)) 

                # thing at the start makes text red

                update_database(user)
                
                current_users.remove(after.id)
                current_playing.remove(user)



def handle_input(split_message):
    # hacky icky code pls ignore
    if split_message[0] == "!topgames":

        if len(split_message) == 3:
            limit = split_message[1]
            month = split_message[2]
            if month not in months:
                output = "invalid month"
            else:
                output = top_games(limit, month)

        elif len(split_message) == 2: 
            if split_message[1].lower() in months:
                month = split_message[1]
                output = top_games(month = month)
            else:
                limit = split_message[1]
                output = top_games(limit)

        elif len(split_message) == 1:
            output = top_games()

        else: 
            output = "incorrect number of parameters"

    elif split_message[0] == "!help":
        output = " `!topgames [limit] [month]`"

    return output

    

client.run(TOKEN)
