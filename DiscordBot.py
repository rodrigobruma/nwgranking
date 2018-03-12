import discord,asyncio
from discord.ext import commands

description="I'm a bot! Here are some commands:"
bot = commands.Bot(command_prefix='!',description=description)

startup_extensions = ['cogs.pubg']

@bot.event
async def on_ready():
	print('Logged in as: {}'.format(bot.user.name))
	print('User ID: {}'.format(bot.user.id))
	await bot.change_presence(game=discord.Game(name='!help - for information'))
	for server in bot.servers:
		print ('Bot connected to: {}'.format(server.name))
	print('------')

if __name__ == "__main__":
	for extension in startup_extensions:
		try:
			bot.load_extension(extension)
			print('Loaded {}'.format(extension))
		except Exception as e:
			exc = '{}: {}'.format(type(e).__name__, e)
			print('Failed to load extension {}\n{}'.format(extension, exc))


	bot.run('TOKEN')
