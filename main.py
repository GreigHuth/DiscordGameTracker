import discord
import logging
import sys
from gametracker import gametracker
from config.config import TOKEN

intents = discord.Intents(presences=True,messages=True,members=True, guilds=True, voice_states=True, dm_messages=True)

#logging shite
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='gt.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#I'm just playing games
#I know that's plastic love
#Dance to the plastic beat
#Another morning comes


# TODO
# optimise the commands
# make commands  more object oriented
# restructure database
# 


if TOKEN == "":
    print("TOKEN not found, please add it in the config.py file.")
    sys.exit(0)


client = gametracker(intents=intents)
client.run(TOKEN)
