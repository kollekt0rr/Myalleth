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
                roll = d20.roll('1d100')
                rolls.append(roll.total)
            return rolls
        
        def loot_from_rolls(loot_table):

            rolls = roll_for_n_creatures(total_creatures)
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
            if loot_table == 'loot_tier_1':
                for r in loot_string:
                    rr = d20.roll(str(r)) 
                    loot_r.append(str(rr.total))
                results = [lr + lt for lr, lt in zip(loot_r, loot_type)] 
           
            else:
                long_loot = []
                for r in loot_string:
                    r = r.split('+')
                    long_loot.extend(r)
                loot_one = long_loot[::2]
                loot_two = long_loot[1::2]
            
                l1 = []
                for l in loot_one:
                    lr = d20.roll(str(l))
                    l1.append(str(lr.total))

                l2 = []
                for l in loot_two:
                    if l != ' ':
                        lr = d20.roll(str(l))
                        l2.append(str(lr.total))
                    else:
                        l2.append('')

                long_type = []
                for t in loot_type:
                    t = t.split('+')
                    long_type.extend(t)

                    type_1 = long_type[::2]
                    type_2 = long_type[1::2]

                pair_1 = [i + j for i, j in zip(l1, type_1)]
                pair_2 = [i + j for i, j in zip(l2, type_2)]
                results =[i +', '+ j for i, j in zip(pair_1,pair_2)]
            
            Mystra_String = 'You have looted: ' + ', '.join(results).replace(' ,', ' ') + ' from ' + total_creatures + ' ' + creature_name.capitalize()+'!'
            
            connc.close()

            return Mystra_String

        creature_name = str(creature_name).lower()

        connc = sqlite3.connect(str(getenv('db')))
        c = connc.cursor()
        c.execute('SELECT creature_cr FROM creatures WHERE creature_name = :creature_name', {'creature_name': creature_name})
        creature_cr = c.fetchone()
        creature_cr = float(creature_cr[0])
        
        if creature_cr <= 4:

            loot = loot_from_rolls('loot_tier_1')

        elif creature_cr <= 10:

            loot = loot_from_rolls('loot_tier_2')
            
        elif creature_cr <=16:
            
            loot = loot_from_rolls('loot_tier_3')
        
        else:

            loot = loot_from_rolls('loot_tier_4')
        
        await inter.response.send_message(loot)

