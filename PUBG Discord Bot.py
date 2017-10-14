#install the discord and pubg-tracker python wrappers using 'pip' first

import discord
from discord.ext import commands
from pypubg import core

client = discord.Client()
api = core.PUBGAPI("PUBG_Tracker API Key") #put in your PUBG API key from here https://pubgtracker.com/site-api

@client.event
async def on_message(message):
	pass
	if message.content.lower().startswith(('!pubg')):
		#Read user input in message. Format is PlayerName, Game Mode, Region
		default=['squad-fpp','na']
		info=[]
		info=message.content.split(" ")
		try:
			player_name=info[1]
		except:
			print("username incorrect")
		try:
			match=info[2]
		except:
			match=default[0]
		try:
			region=info[3]
		except:
			region=default[1]

			#Gets data from the PUBG API
		try:
			player=api.player(player_name)
			pstats=player["Stats"]
			for x in pstats:
				if x['Region']==region.lower() and x['Match']==match.lower():
					count=0
					stats_list={}
					max=len(x['Stats'])
					while count < max:
						stats=x['Stats'][count]
						for key,value in stats.items():
							if key=='label':
								label=value
							if key=='rank' and count==9:
								stats_list[key]=value
							if key=='displayValue' and label!=None:
								stats_list[label]=value
						count+=1
				#print(stats_list) #uncomment to see list of available player stats

			#Outputs formatted message to Discord
			embed = discord.Embed(title=player_name.upper(), description=str(region.upper() +"-"+match.upper()) , color=0x00ff00)
			embed.set_thumbnail(url=player['Avatar'])
			embed.add_field(name="Rank", value=stats_list['rank'], inline=True)
			embed.add_field(name="Skill Rating", value=stats_list['Rating'], inline=True)
			embed.add_field(name="Win Rate", value=stats_list['Win %'], inline=True)
			embed.add_field(name="K/D", value=stats_list['K/D Ratio'], inline=True)
			await client.send_message(message.channel, embed=embed)
		except:
			msg='{0.author.mention} something went wrong! Make sure you entered the player name and information corectly.\nThe format is:"!pubg PlayerName GameMode Region"\nDefault Mode: '+default[0]+'\nDefault Region: '+default[1]
			await client.send_message(message.channel, msg.format(message))
client.run('Discord Bot Secret') #put in your discord bots secret ID. Info here: https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token
