import discord
import requests,json

pubg_api_key=None

#change default values, use filters from below. Keep format [mode,region,season]
default = ['squad-fpp','na','2017-pre5']

#filters from PUBG tracker
modes = ['solo','duo','squad','solo-fpp','duo-fpp','squad-fpp']
regions = ['as', 'sea', 'na', 'agg', 'eu', 'krjp','sa','oc']
seasons = ['2017-pre1','2017-pre2','2017-pre3','2017-pre4','2017-pre5']

def PUBG_API(url,api_key):
	try:
		header={'content-type': "application/json",'trn-api-key': api_key}
		data=requests.get(url,headers=header).json()
		return data
	except BaseException as error:
		print('Unhandled exception: ' + str(error))
		raise

def no_player():
	embed=discord.Embed(title='Error', description='No player name was entered.',color=0xff0000)
	return embed

def pubg_stats(message):

	mode=None
	region=None
	season=None
	players=[]
	output=[]
	message=message[6:]

	#message if no data is entered
	if message==None:
		output.append(no_player())
		return output
	message = message.split()

	#if no API key is entered, it'll let you know
	if pubg_api_key==None or "":
		print('Missing API Key!')
		embed=discord.Embed(title='Error:',description='Missing API Key!')
		output.append(embed)
		return output

	#get player region and match type, if none are put in it uses default values
	for data in message:
		if data in modes:
			mode=data
		if data in regions:
			region=data
		if data in seasons:
			season=data
		if data not in (modes+regions+seasons):
			players.append(data)

	#sets search criteria if none is input, uses default values
	if mode==None:
		mode=default[0]
	if region==None:
		region=default[1]
	if season==None:
		season=default[2]

	#check if playernames are entered
	if len(players)==0:
		output.append(no_player())
		return output

	else:
		#get stats for players requested
		for playername in players:
			pubg_url='https://api.pubgtracker.com/v2/profile/pc/{}?region={}&mode={}&season={}'.format(playername,region,mode,season)
			player=PUBG_API(pubg_url,pubg_api_key)
			criteria=False

			#check for message from PUBG Tracker, I've only seen in for invalid API Keys
			if 'message' in player.keys():
				embed= discord.Embed(title='Message from PUBG Tracker:', description='Error for player {}:\n{}'.format(playername.upper(),player['message']),color=0xff0000)
				embed.to_dict()
				output.append(embed)
				print('Invalid API Key!')
				return output

			#check for errors, usually playername isn't valid
			elif 'error' in player.keys():
				embed= discord.Embed(title='Message from PUBG Tracker:', description='Error for player {}:\n{}'.format(playername.upper(),player['error']),color=0xff0000)
				embed.to_dict()
				output.append(embed)

			else:
				#parse through player stats returned from PUBG Tracker
				for stats in player['stats']:
					if stats['mode']==mode and stats['region']==region and stats['season']==season:
						criteria=True
						stats_list=dict((category['label'],category['displayValue']) for category in stats['stats'])
						stats_list['rank']=stats['stats'][9]['rank']
						#print(stats_list.keys()) #uncomment to see list of available player stats

						#Outputs formatted embed to Discord
						embed = discord.Embed(title=player['nickname'],url='https://pubgtracker.com/profile/pc/{}?region={}'.format(player['nickname'],region), description=str(region.upper() +"-"+mode.upper()) , color=0x00ff00)
						embed.set_thumbnail(url=player['avatar'])
						embed.add_field(name="Rank", value=stats_list['rank'], inline=True)
						embed.add_field(name="Skill Rating", value=stats_list['Rating'], inline=True)
						embed.add_field(name="Win Rate", value=stats_list['Win %'], inline=True)
						embed.add_field(name="K/D", value=stats_list['K/D Ratio'], inline=True)
						embed.to_dict()
						output.append(embed)

				#message if player has no stats with given match or region
				if criteria==False:
					embed= discord.Embed(title='Error:', description='{} has no games with this criteria.\nRegion: {}\nMode: {}'.format(player['nickname'],region,mode),color=0xff0000)
					embed.to_dict()
					output.append(embed)

		return output
