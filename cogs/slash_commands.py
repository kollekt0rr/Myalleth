import disnake
from disnake.ext import commands
import sqlite3
import d20
from os import getenv
from dotenv import load_dotenv

class SlashCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 

    @commands.slash_command(name = 'lootcreature', description = 'Returns loot from monster loot tables for each monster killed')
    async def lootcreature(self, inter, creature_name, total_creatures):
        
        load_dotenv()
        
        def roll_for_n_creatures(total_creatures):
            rolls = []
            while len(rolls) != int(total_creatures):
                roll = d20.roll("1d100")
                rolls.append(roll.total)
            return rolls

        creature_name = str(creature_name).capitalize()

        connc = sqlite3.connect(str(getenv('db')))
        c = connc.cursor()
        c.execute('SELECT creature_cr FROM creatures WHERE creature_name = :creature_name', {'creature_name': creature_name})
        creature_cr = c.fetchone()
        creature_cr = float(creature_cr[0])
        
        if creature_cr <= 4:
            rolls = roll_for_n_creatures(total_creatures)
        elif creature_cr <= 10:
            rolls = roll_for_n_creatures(total_creatures)
        elif creature_cr <=16:
            rolls = roll_for_n_creatures(total_creatures)
        else:
            rolls = roll_for_n_creatures(total_creatures)
        
        await inter.response.send_message(rolls)

