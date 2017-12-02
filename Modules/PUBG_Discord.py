import discord
import requests,json,os

pubg_api_key=None

#change default values, use filters from below. Keep format [mode,region]
class default:
	mode='squad-fpp'
	region='na'
#filters from PUBG tracker
modes = {'solo':'Solo','duo':'Duo','squad':'Squad','solo-fpp':'FP Solo','duo-fpp':'FP Duo','squad-fpp':'FP Squad'}
regions={'na':'[NA] North America','as':'[AS] Asia','sea':'[SEA] South East Asia','krjp':'[KRJP] Korea/Japan','oc':'[OC] Oceania','sa':'[SA] South America'}

def PUBG_API(url):
	try:
		header={'content-type': "application/json",'trn-api-key': pubg_api_key}
		data=requests.get(url,headers=header).json()
		return data
	except BaseException as error:
		print('Unhandled exception: ' + str(error))
		raise

def no_player():
	embed=discord.Embed(title='Error', description='No player name was entered.',color=0xff0000)
	return embed
def error_message(playername,message):
	embed= discord.Embed(title='Message from PUBG Tracker:', description='Error for player {}:\n{}'.format(playername.upper(),message),color=0xff0000)
	embed.to_dict()
	print('Invalid API Key!')
	return embed

def check_api():
	#if no API key is entered, it'll let you know
	if pubg_api_key==None or "":
		print("\nMissing PUBG API Key!!")

def read_json(file_name):
	if file_name.endswith('.json')==False:
		file_name=file_name+'.json'
	if not os.path.isfile(file_name):
		list_name=open(file_name,"w+")
		list_name={}
	else:
		try:
			with open(file_name) as f:
				list_name = json.load(f)
		except ValueError:
			list_name={}
	return list_name

def edit_json(file_name,items):
	if file_name.endswith('.json')==False:
		file_name=file_name+'.json'
	with open(file_name,"w") as f:
		f.write(json.dumps(items))

def pubg_stats(message,match_history=False):
	pubg_ids=read_json('pubg_ids')
	mode=None
	region=None
	players=[]
	output=[]

	#message if no data is entered
	if message==None:
		output.append(no_player())
		return output
	message = message.split()

	#get player region and match type, if none are put in it uses default values
	for data in message:
		if data in modes:
			mode=data
		if data in regions:
			region=data
		if data not in (list(modes)+list(regions)):
			players.append(data)

	#sets search criteria if none is input, uses default values
	if mode==None:
		mode=default.mode
	if region==None:
		region=default.region

	#check if playernames are entered
	if len(players)==0:
		output.append(no_player())
		return output

	else:
		#get stats for players requested
		for playername in players:
			#check if player accountId has been logged and if match history is being requested
			#logging player saves time because the API doesn't have to send a request twice
			if playername in pubg_ids.keys() and match_history==True:
				player=pubg_ids[playername]
			else:
				pubg_url='https://api.pubgtracker.com/v2/profile/pc/{}'.format(playername)
				player=PUBG_API(pubg_url)
				criteria=False
				#logs new player accountId if it's valid
				if playername not in pubg_ids.keys() and ('error'or'message') not in player.keys():
					pubg_ids[playername]={}
					pubg_ids[playername]['accountId']=player['accountId']
					pubg_ids[playername]['nickname']=player['nickname']
					edit_json('pubg_ids',pubg_ids)

			#check for message from PUBG Tracker, I've only seen in for invalid API Keys
			if 'message' in player.keys():
				embed=error_message(playername,player['message'])
				output.append(embed)
				return output

			#check for errors, usually playername isn't valid
			elif 'error' in player.keys():
				embed= discord.Embed(title='Message from PUBG Tracker:', description='Error for player {}:\n{}'.format(playername.upper(),player['error']),color=0xff0000)
				embed.to_dict()
				output.append(embed)

			elif match_history==False:
				#parse through player stats returned from PUBG Tracker
				for stats in player['stats']:
					if stats['mode']==mode and stats['region']==region:
						criteria=True
						stats_list=dict((category['label'],category['displayValue']) for category in stats['stats'])
						stats_list['rank']=stats['stats'][9]['rank']
						#print(stats_list.keys()) #uncomment to see list of available player stats

						#Outputs formatted embed to Discord
						embed = discord.Embed(title=player['nickname'],url='https://pubgtracker.com/profile/pc/{}?region={}'.format(player['nickname'],region), description='{}-{}'.format(regions[region],modes[mode]) , color=0x00ff00)
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

			#will run if requesting match history for a player
			#returns last 3 matches or less if a player doesn't have at least 3 played
			elif match_history==True:
				rnd=0
				top=3
				match_url='https://api.pubgtracker.com/v2/matches/pc/{}'.format(player['accountId'])
				matches=PUBG_API(match_url)
				if 'message' in matches:
					embed=error_message(playername,matches['message'])
					output.append(embed)
					return output
				if len(matches)<top:
					top=len(matches)
				embed = discord.Embed(title=player['nickname'],url='https://pubgtracker.com/history/pc/{}'.format(player['nickname']),description='Results from last {} matches'.format(top), color=0x00ff00)
				#loop through matches and add data to the embeded message
				while rnd < top:
					embed.add_field(name='Region',value=matches[rnd]['regionDisplay'], inline=True)
					embed.add_field(name='Mode',value=matches[rnd]['matchDisplay'], inline=True)
					embed.add_field(name='Kills',value=matches[rnd]['kills'], inline=True)
					if matches[rnd]['wins']==1:
						wins='Yes'
					else:
						wins='No'
					embed.add_field(name='Win',value=wins, inline=True)
					if matches[rnd]['top10']==1:
						top10='Yes'
					else:
						top10='No'
					embed.add_field(name='Top 10',value=top10, inline=True)
					embed.add_field(name='Skill Change',value=matches[rnd]['ratingChange'], inline=True)
					embed.to_dict()
					rnd+=1
				output.append(embed)

	return output
