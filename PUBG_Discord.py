#install the discord and pubg-tracker python wrappers using 'pip' first
import discord
from discord.ext import commands
from pypubg import core

'''
Example of importing function into your bot if file is in the same directory
#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/

import PUBG_Discord

@client.event
async def on_message(message):
	
	if message.content.lower().startswith("!pubg"):
		stats=PUBG_Discord.pubg_stats(message.content.lower())
		for player_stats in stats:
			await client.send_message(message.channel, embed=player_stats)
			
#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/'''

def pubg_stats(message):
	api = core.PUBGAPI("PUBG Tracker API Key") #put in your PUBG API key from here https://pubgtracker.com/site-api
	message = message[6:]
	message = message.split()
	matches = ['solo','duo','squad','solo-fpp','duo-fpp','squad-fpp']
	match=None
	regions = ['as', 'sea', 'na', 'agg', 'eu', 'krjp','sa','oc']
	region=None
	default=['squad-fpp','na']
	players=[]
	output=[]
	
	
	#get player region and match type, if none are put in it uses default values
	for data in message:
		if data in matches:
			match=data
		if data in regions:
			region=data
		if data not in (matches+regions):
			players.append(data)		
		if match==None:
			match=default[0]
		if region==None:
			region=default[1]
	
	if len(players)==0:
		embed=discord.Embed(title='Error', description=str('No player name was entered.'),color=0xff0000)
		output.append(embed)
		
	for player_name in players:
		player=api.player(player_name)
		criteria=False
		
		if 'error' in player.keys():
			if int(player['error'])==True:
				e_type='message'
			else:
				e_type='error'
			embed= discord.Embed(title='Message from PUBG Tracker:', description=str('Error for player "'+player_name.upper()+'":\n'+str(player[e_type])),color=0xff0000)
			embed.to_dict()
			output.append(embed)
			
		else:
			for stats in player['Stats']:
					if stats['Match']==match and stats['Region']==region and stats['Season']==player['defaultSeason']:
						criteria=True
						stats_list=dict((category['label'],category['displayValue']) for category in stats['Stats'])
						stats_list['Rank']=stats['Stats'][9]['rank']
						#print(stats_list) #uncomment to see list of available player stats
					
						#Outputs formatted message to Discord
						embed = discord.Embed(title=player['PlayerName'], description=str(region.upper() +"-"+match.upper()) , color=0x00ff00)
						embed.set_thumbnail(url=player['Avatar'])
						embed.add_field(name="Rank", value=stats_list['Rank'], inline=True)
						embed.add_field(name="Skill Rating", value=stats_list['Rating'], inline=True)
						embed.add_field(name="Win Rate", value=stats_list['Win %'], inline=True)
						embed.add_field(name="K/D", value=stats_list['K/D Ratio'], inline=True)
						embed.to_dict()
						output.append(embed)
						
			#message if player has no stats with given match or region			
			if criteria==False:
				embed= discord.Embed(title='Error:', description=str(player['PlayerName']+' has no games with this criteria.\nRegion: '+region+'\nMatch: '+match),color=0xff0000)
				embed.to_dict()
				output.append(embed)
			
	return output
