import disnake
from disnake.ext import commands
from random import randint
from os import getenv
from dotenv import load_dotenv
#from cogs import *
import d20

load_dotenv()
DESTINATION = int(getenv('CHANNEL_ID_NUMBER'))

bot = commands.Bot(command_prefix = '$', intents = disnake.Intents.all())

@bot.event
async def on_ready():
    print('Mystra returns from the weave!')
    welcome = await bot.fetch_channel(DESTINATION)
    await welcome.send('Mystra returns from the weave!')

@bot.command(aliases = ['shutdown', 'kick', 'close', 'quit'])
async def banish(ctx):
    await ctx.send(f'{ctx.author.display_name} has banished Mystra to the weave')
    await bot.close()

@bot.command()
async def loot(ctx, creatures: str, total: int):
    
    rolls = []
    while len(rolls) != total:
       roll =  d20.roll("1d100")
       rolls.append(roll.total)
    
    for roll in rolls:
        if roll <= 50:
            
    await ctx.send(rolls)

bot.run(getenv('DISCORD_TOKEN_STRING'))

