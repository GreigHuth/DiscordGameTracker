#bot to keep track of how many and how often games are played on discord

import discord

TOKEN = "NTM5MTQwNTExMjM2MzU4MTQ0.Dy-Bdg.ZEiEWfMm_ji1I0qdpbDqJDAJSog"
client = discord.Client()

@client.event
async def on_ready():
	print("The bot is ready!")
	await client.change_presence(game=discord.Game(name="Making a bot"))

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if message.content == "!time":
		game = message.author.game
		print(type(game))
		if game is None:
			await client.send_message(message.channel, "no game")
		await client.send_message(message.channel, hash(game))

@client.event
async def on_member_update(before, after):
	print (before.game)
	print (after.game)

client.run(TOKEN)