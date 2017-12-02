import discord,asyncio
from Modules import PUBG_Discord


client = discord.Client()

PUBG_Discord.pubg_api_key='pubg_api_key'

@client.event
async def on_ready():
	print('Logged in as: '+client.user.name)
	print('Bot ID: '+client.user.id)
	for server in client.servers:
		print ("Connected to server: "+ server.name)
	print('------')
	PUBG_Discord.check_api()

@client.event
async def on_message(message):

	if message.content.lower().startswith('!pubg_matches'):
		shorten=message.content[len('!pubg_matches'):].lower().strip()
		players=PUBG_Discord.pubg_stats(shorten,match_history=True)
		for player in players:
			await client.send_message(message.channel,embed=player)

	if message.content.lower().startswith('!pubg_stats'):
		shorten=message.content[len('!pubg_stats'):].lower().strip()
		players=PUBG_Discord.pubg_stats(shorten)
		for player in players:
			await client.send_message(message.channel,embed=player)

client.run('Discord_API_Key')
