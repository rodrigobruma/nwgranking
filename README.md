# PUBG-Discord-Bot

# How to use:
- Download this repo or just pubg.py and import it into your bot if you already have one.
- Download [Discord.py](https://github.com/Rapptz/discord.py)
- [Get a Discord code to use a bot and add it to your server.](https://discordapp.com/developers/docs/topics/oauth2#bots)  There are plenty of tutorials on how to set one up on YouTube.
- Put your code in this line: `bot.run('Discord API Key')`
- Use Pip to install BeautifulSoup: `pip install bs4`
- Edit default values in pubg.py if you want. Current Default: `mode='squad-fpp', region='na'`
- If everything goes well, it will connect and you can call it using `!stats {playername}` with any valid filters.

![example](https://imgur.com/a/mSpUg)

# What's new:
- Remade using the [pubg.op.gg](https://pubg.op.gg/) API since the PUBG Tracker API has been down for a while.
- Better use of async
- Basic bot setup for cogs for easy additions.

# Features:
- Can do multiple players at one time.
- Can change search criteria using the valid filters:

  `modes = ['solo','duo','squad','solo-fpp','duo-fpp','squad-fpp']`

  `regions = ['as', 'sea', 'na', 'agg', 'eu', 'krjp','sa','oc']`

- Should correct most errors and at least output something.

# Issues:
- If your name is one of the game modes, or regions this won't work for you.
