#MarketBot
A bot providing access to a public listing of items being sold across various Clemson Discord servers


Originally created for the 2020 Clemson "Hello World" Hackathon by **Nathan Brown, Alex Shelton, Darin Spitzer, and John Mathews.**

MarketBot is a Python-based Discord bot intended for buying and selling miscellanous items across Clemson.
When added to your Discord server, MarketBot gives your server's users access to a list of items which are being sold.
This list is shared across all servers who have added MarketBot. This means that when someone in a Discord server you're not in lists an item, you will still be able to see this listing!

# COMMANDS
	$market			-	Displays information on how to use MarketBot
  
	$sell <item>	-	Allows you to publicly list an item for sale
  
	$remove <item>-	Allows you to remove your item from being listed
  
	$viewAll		-	Displays basic information on all the items which are currently listed
  
	$view <item>	-	Displays more detailed information on the specified item

# INSTALLATION
	MarketBot requires Python 3+ ()
	MarketBot requires discord.py to function. Install it using "python -m pip install -U discord.py"

# USAGE:
	Run "python marketbot.py" to launch the bot

MarketBot was built using the publicly-available Discord.py API:
https://github.com/Rapptz/discord.py
