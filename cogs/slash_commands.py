import disnake
from disnake.ext import commands
import sqlite3
import d20
from os import getenv
from dotenv import load_dotenv
from random import randint

class Venture(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description = 'Checks if user has existing character in game system.')
    async def join(self, inter):
        
        await inter.response.send_message(f'{inter.author.id} is playing the game as CHARACTER')
        # check here to see if user has made character yet.
        
    #@commands.slash_command(        
    #async def 

class Looting(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 
        
        load_dotenv()
    
    @commands.slash_command(name = 'lootcreature', description = 'Returns loot from monster loot tables for each monster killed')
    async def lootcreature(self, inter, creature_name: str, total_creatures: int = commands.Param(gt=0)):
   
        def loot_from_rolls(loot_table):

            rolls = [randint(1, 100) for x in range(total_creatures)]
            
            #This is bad, do not do this if using in environment where you don't trust users 
            #This can lead to SQL injection if you take this code please rewrite this portion :D
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
            
            Myalleth_String = inter.author.display_name + ' has looted: ' + ', '.join(results).replace(' ,', ' ') + ' from ' + str(total_creatures) + ' ' + creature_name.capitalize()+'!'
            
            con.close()

            return Myalleth_String

        creature_name = str(creature_name).lower()

        con = sqlite3.connect(str(getenv('DB')))
        c = con.cursor()
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

    @commands.slash_command(name = 'lootlair', description = 'Returns loot from monster lair loot tables for monster type specified')
    async def lootlair(self, inter, creature_name):
        
        loot = 'Howdy lair looter'

        await inter.response.send_message(loot)

    @commands.slash_command(name = 'rules', description = 'Returns rulings as stated in rulebooks')
    async def rules(self, inter, requested_rule):

        rule = 'This will return a rule at some point.'

        await inter.response.send_message(rule)

class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name = '3da', description = 'Initiate a game of Three-Dragon Ante')
    async def TDA(self, inter):
        
        result = 'Gambling Time!'
        
        await inter.response.send_message(result)
