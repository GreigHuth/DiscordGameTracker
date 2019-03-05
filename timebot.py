#bot to keep track of how many and how often games are played on discord
import discord
import logging
import time
from user import *
from update_database import *
from commands import * 

logging.basicConfig(level=logging.INFO)#logs errors and debug info


#TODO
#implement sql stuff[x]
#implement commands to actually use the bot[ ]
#Add functionality to allow people to pm the bot and get thier own personal gametimes[]
#make the overall bot more presentable[]
#pitch to people[]
#get a better name[]
#get a profile pic[]
#write some bloody documentation[]
#neated up the code[]



#global variables-------------------------------------------
current_playing = []


# token for test server
TOKEN = "NTUyNTAxOTQ0MTQ1NDEyMDk2.D2AeCg.fT6rMT_-fzN2Ms9LcBZB6-3ucYE"


client = discord.Client()

@client.event
async def on_ready():
	print("The bot is ready!")
	await client.change_presence(game=discord.Game(name="E A R L Y  A C C E S S"))

@client.event
async def on_message(message):
	pass

	


@client.event
async def on_member_update(before, after):
	if before.bot == True: # if the user is a bot ignore it
		return


	if before.game == None and after.game != None : # a user has just started playing a game

		print ("UPDATE: user %s has started playing %s." % (before.name, after.game.name))

		id = before.id
		game = after.game.name 
		start = time.time()
		end = None

		user= User(id, game, start, end) #creates new user
		current_playing.append(user) # adds new user to list of people currently playing games
	

	elif after.game == None and before.game != None : # a user has just stopped playing a game
		print ("UPDATE: user %s has stopped playing %s." %(after.name, before.game.name ))

		end = time.time() 
		for user in current_playing:
			# find current user in list of users playing games

			if after.id == user.id and before.game.name == user.game: 

				user.end = end # time user stopped playing the game
				time_played = user.end - user.start # total time the game was played 
				user.end = end
				print ("UPDATE: user %s played %s for %d seconds." % (after.name, before.game.name, time_played)) 
				update_database(user)
				current_playing.remove(user)



	

client.run(TOKEN)