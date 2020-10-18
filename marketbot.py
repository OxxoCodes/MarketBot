#Title: Hello World - cuhackit 10/17/2020
#Authors: Team 15 (Plethora of Maniacs): Nathan, Darin, Alex, John
#Project: MarketBot
#Version: Beta 1.0

#TO-DO: Add ability to add descriptions
#TO-DO: Limit submissions/day on MarketBot; maybe add pictures eventually


#import libraries: including discord API
import json
import discord
from discord.ext import commands
import random

#market description:
description = "A marketplace bot for Clemson" 
#Set default bot intents
intents = discord.Intents.default() 

#bot prefix: user enters '$' to enter in commands for marketBot
bot = commands.Bot(command_prefix='$', description=description, intents=intents)

#function: opens .json file for the marketBot to read from
def readListings():
    with open('listings.json', 'r') as f:
        return json.loads(f.read())
        
#function: writes the user listing to the .json file
def writeListings(x):
    with open('listings.json', 'w') as f:
        f.write(json.dumps(x))

#event: When the bot loads up, execute the following
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    #Changes status to idle for bot when bot not in use. Also displays the Game state
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Use $market for help'))

#$market command: Removes listings from the .json file
@bot.command()
async def remove(ctx, num:int):
    listings = readListings()
    if num <= 0:
        await ctx.send("**ERROR:** Item number cannot be less than or equal to 0.")
        return
    if listings[0]["numberOfListings"] < num:
        await ctx.send("**ERROR:** Item not recognized!")
        return
    if (listings[num]['userid'] == ctx.author.id):
        listings.pop(num)
        listings[0]["numberOfListings"] = int(listings[0]["numberOfListings"]) - 1
        writeListings(listings)
        await ctx.send('Item has been removed!')
    else:
        await ctx.send('**ERROR:** You are not the user who made this listing.')

#$market command: Prints the list of commands the user can input
@bot.command()
async def market(ctx):
    output = """```$sell <Item Name> <Price> <Contact Info>``` - Spaces split up the parameters, use underscores in the item name or contact if needed.

                ```$remove <Item Number>``` - Remove one of your listings from the public list.

                ```$view <Item Number>``` - View more information on an item. 

                ```$viewAll``` - Lists all items that are currently being sold. """
    embed = discord.Embed(title='List of Commands:  :coin:',
                          description=output, colour = discord.Colour.blue())
    embed.set_image(url='https://cdn.discordapp.com/avatars/767044968878440479/0ef76e39c69d1815a32d1697d7df070b.png')
    await ctx.send(embed=embed)

#$market command: Lets user list their items to $market/.json file
# $sell item_Name price contact
@bot.command()
async def sell(ctx, item:str, price:str, contact:str):
    invalidChars = ["*", "<", ">", ",", "\\", "!"]
    for invalid in invalidChars:
        if invalid in item or invalid in price or invalid in contact:
            await ctx.send("**ERROR:** Please do not enter symbols.")
            return
    listings = readListings()

    listings.append({ "Listing":item, "Price":price, "Contact":contact, "userid":ctx.author.id})
    listings[0]["numberOfListings"] = int(listings[0]["numberOfListings"]) + 1
    author = ctx.author
    
    #Wait on response from user to enter description
    def check(m):
        return m.author == author
    await ctx.send("Awesome! Please enter a brief description of your item.")
    msg = await bot.wait_for('message', check=check)
    
    numOfListings = int(listings[0]["numberOfListings"])
    listings[numOfListings]['Description'] = msg.content

    writeListings(listings)
    embed = showListing(int(listings[0]["numberOfListings"]))
    await ctx.send("Listing added!")
    await ctx.send(embed=embed)

#function: returns the embed information
def showListing(num):
    listings = readListings()
    output = ""
    for key in listings[num]:
        if key != "userid":
            output += "**" + key + "**: " + str(listings[num][key]) + "\n"
    embed = discord.Embed(title='Viewing Item #'+str(num)+'  :eyes:',
                          description=output, colour = discord.Colour.blue())
    return embed

#function: print error message for user whenever invalid argument is passed
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.BadArgument):
        await ctx.send("ERROR: Invalid argument. Please run **$market** for information on how to use MarketBot's commands.")

#Views the listing the user specifies
@bot.command()
async def view(ctx, num:int):
    if num == 69420 or num == 42069:
        await ctx.send("haha funny number lol")
        return
    if num <= 0:
        await ctx.send("**ERROR:** Item number cannot be less than or equal to 0.")
        return
    embed = showListing(num)
    await ctx.send(embed=embed)

#Prints all listings in the listings.json file and displays their listing & price
@bot.command()
async def viewAll(ctx):
    listings = readListings() #Read file as string and parse as json
    numOfListings = listings[0]["numberOfListings"]
    output = ""
    for i in range(1,int(numOfListings)+1): #for loop: displays the listing + price for user
        listing = listings[i]["Listing"] 
        price = listings[i]["Price"]
        output += str(i) + ")  **" + listing + "**: " + price + "\n\n"
    embed = discord.Embed(title='All Current Listings  :fire:',
                          description=output, colour = discord.Colour.blue())
    await ctx.send(embed=embed)

#Unique bot token.
bot.run('token')