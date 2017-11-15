import discord,asyncio
from Modules import PUBG_Discord


client = discord.Client()

PUBG_Discord.pubg_api_key='PUBG API Key'

@client.event
async def on_ready():
	print('Logged in as: '+client.user.name)
	print('Bot ID: '+client.user.id)
	for server in client.servers:
		print ("Connected to server: "+ server.name)
	print('------')


@client.event
async def on_message(message):
	if message.content.lower().startswith('!pubg'):
		players=PUBG_Discord.pubg_stats(message.content.lower())
		for player in players:
			await client.send_message(message.channel,embed=player)


client.run('Discord API Key')
