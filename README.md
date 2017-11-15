# PUBG-Discord-Bot

# How to use:
- Download this repo or just PUBG_Discord.py and import it into your bot if you already have one.
- [Get a Discord code to use a bot and add it to your server.](https://discordapp.com/developers/docs/topics/oauth2#bots)  There are plenty of tutorials on how to set one up on YouTube.
- Put your code in this line: `client.run('Discord API Key')`
- [Get a PUBG Tracker API key.](https://pubgtracker.com/site-api)
- Put your key in this line: `PUBG_Discord.pubg_api_key='PUBG API Key'`
- Edit default values in PUBG_Discord.py if you want. Currently: `default = ['squad-fpp','na','2017-pre5']`
- If everything goes right it will connect and you can call it using '!pubg {playername}' plus any filters if you don't want to use the default ones.

# What's new:
- Updated to use V2 of the PUBG Tracker API
- You no longer need to install the pypubg repo for it to work
- Includes basic bot code to get you started, the only additional thing you need is [Discord](https://github.com/Rapptz/discord.py)
- Link to a players PUBG Tracker profile are given in the stat output
- Better error detection, hopefully

# Features:
- Can do multiple players at one time.
- Can change search criteria using the valid filters:

  `modes = ['solo','duo','squad','solo-fpp','duo-fpp','squad-fpp']`
  
  `regions = ['as', 'sea', 'na', 'agg', 'eu', 'krjp','sa','oc']`
  
  `seasons = ['2017-pre1','2017-pre2','2017-pre3','2017-pre4','2017-pre5','2017-pre6']`
  
- Should correct most errors and at least output something.
- Outputs Errors given by PUBGTracker. ie. The API is down, sometimes, or player cant be found.

# Issues:
- If your name is one of the game modes, regions, or seasons, this won't work for you.
- If the PUBG Tracker API is down, it might not output anything.
- Seasons need to be manually updated when they end to get the latest stats. This wasn't an issue in v1 and I've emailed them to ask if they'll fix it. 
