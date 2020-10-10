import discord
import logging
import sys
from gametracker import gametracker
from config.config import TOKEN

logging.basicConfig(level=logging.INFO)  # logs errors and debug info

#I'm just playing games
#I know that's plastic love
#Dance to the plastic beat
#Another morning comes



# TODO
# implement sql stuff[x]
# implement commands to actually use the bot[x]
# Add functionality to allow people to pm the bot and get thier own personal gametimes[]
# Add commands so people can query gametimes about specific games[]
# get a better name[x]
# get a profile pic[]
# changed it so it displays the start and stop messages in different colours[x]
# implent a way to gradually add times to db(say every 10 mins)[]


if TOKEN == "":
    print("TOKEN not found, please add it in the config.py file.")
    sys.exit(0)


client = gametracker()
client.run(TOKEN)
