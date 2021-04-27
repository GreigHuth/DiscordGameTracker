import discord
from .Command import Command


class bot_help(Command):

    def __init__(self):
        super().__init__(None, None)


    def execute(self, args):
        title =  "I'm Gametracker, I track the games you play using status messages\n"

        content =  "!mygames  - Your top ten played games this month\n"
        content += "!topgames - Top ten most played games in the server\n"
        content += "!topusers - Top ten users in the server\n"
        content += "\n"

        message= discord.Embed(title=title, type="rich", description=content, colour=self.embed_colour)

        message.set_footer(text="My code is here: https://github.com/GreigHuth/GameTracker")

        return message



