import logging
from os import getenv
from random import randint

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import CommandSyncFlags
from dotenv import load_dotenv

cogs = ['cogs']

load_dotenv()
DESTINATION = int(getenv('CHANNEL_ID_NUMBER'))

command_sync_flags = commands.CommandSyncFlags.default()

bot = commands.Bot(command_prefix = '$', intents = disnake.Intents.all(), command_sync_flags = command_sync_flags)

@bot.event
async def on_ready():
    print('Mystra returns from the weave!')
    welcome = await bot.fetch_channel(DESTINATION)
    await welcome.send('Mystra returns from the weave!')

for cog in cogs:
    bot.load_extension(cog)

@bot.slash_command()
async def banish(ctx):
    for cog in cogs:
        bot.unload_extension(cog)
    await ctx.send(f'{ctx.author.display_name} has banished Mystra to the weave')
    await bot.close()

bot.run(getenv('DISCORD_TOKEN_STRING'))

