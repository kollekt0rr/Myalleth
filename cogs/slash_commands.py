import disnake
from disnake.ext import commands
import d20

class SlashCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name = 'loot', description = 'Returns loot from monster loot tables for each monster killed')
    async def loot(self, inter, creature_name, total_creatures):

        rolls = []
        while len(rolls) != int(total_creatures):
            roll = d20.roll("1d100")
            rolls.append(roll.total)

        rarity = []
        for roll in rolls:
            if roll == 1:
                rarity.append("Critical Failure")
                break
            elif roll <= 46:
                rarity.append("Common")
            elif roll <= 70:
                rarity.append("Uncommon")
            elif roll <= 90:
                rarity.append("Rare")
            elif roll <= 99:
                rarity.append("Very Rare")
            else:
                rarity.append("Legendary")

        pulls = {rolls[i]: rarity[i] for i in range(len(rolls))}
        
        await inter.response.send_message(pulls)

