import discord
import logging
import sys
from gametracker import gametracker
from config.config import TOKEN


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
# get a better name[x]
# get a profile pic[]
# MAKE THE COMMANDS MORE OBJECT ORIENTED


if TOKEN == "":
    print("TOKEN not found, please add it in the config.py file.")
    sys.exit(0)


client = gametracker()
client.run(TOKEN)
