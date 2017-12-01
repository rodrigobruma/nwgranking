# PUBG-Discord-Bot

# How to use:
- Download this repo or just PUBG_Discord.py and import it into your bot if you already have one.
- Download [Discord.py](https://github.com/Rapptz/discord.py)
- [Get a Discord code to use a bot and add it to your server.](https://discordapp.com/developers/docs/topics/oauth2#bots)  There are plenty of tutorials on how to set one up on YouTube.
- Put your code in this line: `client.run('Discord API Key')`
- [Get a PUBG Tracker API key.](https://pubgtracker.com/site-api)
- Put your key in this line: `PUBG_Discord.pubg_api_key='PUBG API Key'`
- Edit default values in PUBG_Discord.py if you want. Currently: `default = 'squad-fpp','na'`
- If everything goes right it will connect and you can call it using `!pubg_stats {playername}` Filters are ignored

# What's new:
- It will grab past matches (default is 3) played for a player with `!pubg_matches {playername}` with link to players PUBG Tracker match profile
- It will store players nicknames and account ids in a separate file for pulling matches. This prevents sending two requests to the API, faster responses.

# Features:
- Can do multiple players at one time.
- Can pull data for past matches for a player. Default is latest 3 matches.
- Can change search criteria using the valid filters:

  `modes = ['solo','duo','squad','solo-fpp','duo-fpp','squad-fpp']`

  `regions = ['as', 'sea', 'na', 'agg', 'eu', 'krjp','sa','oc']`

- Should correct most errors and at least output something.
- Outputs Errors given by PUBGTracker. ie. The API is down, sometimes, or player cant be found.


# Issues:
- If your name is one of the game modes, or regions this won't work for you.
- If the PUBG Tracker API is down, it might not output anything.
