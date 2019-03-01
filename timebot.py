#bot to keep track of how many and how often games are played on discord
import discord
import logging
import time
from user import * 

logging.basicConfig(level=logging.INFO)#logs errors and debug info


#TODO
#implement sql stuff
#implement commands to actually use the bot



#global variables-------------------------------------------
current_playing = []


# token for test server
TOKEN = "NTM5MTQwNTExMjM2MzU4MTQ0.Dy-Bdg.ZEiEWfMm_ji1I0qdpbDqJDAJSog"


client = discord.Client()

@client.event
async def on_ready():
	print("The bot is ready!")
	await client.change_presence(game=discord.Game(name="tick, tock"))

@client.event
async def on_message(message):
	pass


@client.event
async def on_member_update(before, after):
	if before.bot == True: # if the user is a bot ignore it
		return

	if before.game == None: # user has just started playing a game
		print ("UPDATE: user %s has started playing %s." % (before.name, after.game.name))

		id = before.id
		game = after.game.name 
		start = time.time()
		end = None

		user= User(id, game, start, end) #creates new user
		current_playing.append(user) # adds new user to list of people currently playing games
	

	elif after.game ==  None: # user has just stopped playing a game
		print ("UPDATE: user %s has stopped playing %s." %(after.name, before.game.name ))

		end = time.time() 
		for user in current_playing:
			# find current user in list of users playing games

			if after.id == user.id and before.game.name == user.game: 

				user.end = end # time user stopped playing the game
				time_played = user.end - user.start # total time the game was played 
				current_playing[user].end = end
				print ("UPDATE: user %s played %s for %d seconds." % (user.name, before.game.name, time_played)) 

				current_playing.remove(user)



	

client.run(TOKEN)