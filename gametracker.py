# bot to keep track of how many and how often games are played on discord
# made by gurg
import discord
import time
import re
from user import *
from database_stuff.update_database import update_database
from generate_output import generate_output






# global variables-------------------------------------------



class gametracker(discord.Client):

    current_users = []
    current_playing = []

    
    async def on_ready(self):
        print("The bot is ready!")
        await self.change_presence(activity=discord.Game(name="Selling your data..."))


    async def on_message(self, message):

        if message.author.id == self.user.id:  # dont trigger on own messages, redundant? yeah but i cba testing
            return


        split_input = message.content.split()

        output = generate_output(split_input, message)

        await message.channel.send()

    
    async def on_member_update(self, before, after):
        c_time = time.strftime("%H:%M:%S")  # current time

        if before.bot == True:  # if the user is a bot ignore it
            return

        elif before.game == None and after.game != None and before.id not in current_users:
            # checks to see if user has started playing a game and is not already playing one

            print("\033[1;32;40m%s: user %s has started playing %s." %
                (c_time, before.name, after.game.name))
            # The thing at the start makes the text green

            id = before.id
            game = after.game.name
            start = time.time()
            end = None

            # add id to list of people currently playing games
            self.current_users.append(id)
            user = User(id, game, start, end)  # creates new user
            # adds new user to list of people currently playing games
            self.current_playing.append(user)

        elif after.game == None and before.game != None:  # a user has just stopped playing a game

            end = time.time()
            for user in self.current_playing:
                # find current user in list of users playing games

                if after.id == user.id and before.game.name == user.game:

                    user.end = end  # time user stopped playing the game
                    time_played = user.end - user.start  # total time the game was played
                    user.end = end

                    print("\033[1;31;40m%s: user %s played %s for %d seconds." % (
                        c_time, after.name, before.game.name, time_played))

                    # thing at the start makes text red

                    update_database(user)

                    self.current_users.remove(after.id)
                    self.current_playing.remove(user)

    async def update_db(self):
        return
