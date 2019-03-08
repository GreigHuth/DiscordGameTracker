#bot to keep track of how many and how often games are played on discord
#made by gurg
import discord
import sys
import logging
import time
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
#get a profile pic[x]
#write some bloody documentation[x]
#neaten up the code[]
#implement commands better[]



#global variables-------------------------------------------
current_playing = []

if TOKEN ==  "":
	print ("TOKEN not found, please add it in the config.py file.")
	sys.exit(0)
	
client = discord.Client()

@client.event
async def on_ready():
	print("The bot is ready!")
	await client.change_presence(game=discord.Game(name="V E R S I O N 1.0"))

@client.event
async def on_message(message):
	if message.content == "!topgames5":
		await client.send_message(message.channel, top_games(5))

	if message.content == "!topgames10":
		await client.send_message(message.channel, top_games(10))

	if message.content == "!help":
		await client.send_message(message.channel, " i need somebody.(only command is !topgames(5|10))")

@client.event
async def on_member_update(before, after):
	c_time = time.strftime("%H:%M:%S") #current time

	if before.bot == True: # if the user is a bot ignore it
		return

	if before.game == None and after.game != None : # a user has just started playing a game
		
		print ("%s: user %s has started playing %s." % (c_time, before.name, after.game.name))

		id = before.id
		game = after.game.name 
		start = time.time()
		end = None

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
				print ("%s: user %s played %s for %d seconds." % (c_time,after.name, before.game.name, time_played)) 
				update_database(user)
				current_playing.remove(user)



	

client.run(TOKEN)