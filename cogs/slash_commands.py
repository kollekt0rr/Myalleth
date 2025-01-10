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
        
        def roll_for_n_creatures(creature_cr, total_creatures):
            dice = '1d{die_type}'
            dice.format(die_type = creature_cr)

            rolls = []
            while len(rolls) != int(total_creatures):
                roll = d20.roll(dice.format(die_type = creature_cr))
                rolls.append(roll.total)
            return rolls
        
        def loot_from_rolls(creature_cr, loot_table):

            rolls = roll_for_n_creatures(creature_cr, total_creatures)
            s = f"SELECT * FROM {loot_table} WHERE roll = :roll"

            loot = []
            for roll in rolls:
                c.execute(s, (roll, ))
                loot.append(list(c.fetchone())) 
           
            for i in range(len(loot)):
                del loot[i][0]
            
            for roll in loot:
                loot_string, loot_type = zip(*loot)
            
            loot_r = []
            for r in loot_string:
                rr = d20.roll(str(r)) 
                loot_r.append(str(rr.total))
            
            results = [lr + lt for lr, lt in zip(loot_r, loot_type)] 
            
            
            Mystra_String = 'You have looted: ' + ', '.join(results) + ' from ' + total_creatures + ' ' + creature_name+'!'
            
            return Mystra_String

        creature_name = str(creature_name).capitalize()

        connc = sqlite3.connect(str(getenv('db')))
        c = connc.cursor()
        c.execute('SELECT creature_cr FROM creatures WHERE creature_name = :creature_name', {'creature_name': creature_name})
        creature_cr = c.fetchone()
        creature_cr = float(creature_cr[0])
        
        if creature_cr <= 4:

            loot = loot_from_rolls(5, 'loot_tier_1')

        elif creature_cr <= 10:

            loot = loot_from_rolls(5, 'loot_tier_2')
            
        elif creature_cr <=16:
            
            loot = loot_from_rolls(4, 'loot_tier_3')
        
        else:

            loot = loot_from_rolls(3, 'loot_tier_4')
        
        await inter.response.send_message(loot)

