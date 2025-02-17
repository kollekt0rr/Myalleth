from .slash_commands import Venture, Looting, Games

def setup(bot):
    bot.add_cog(Venture(bot)) 
    bot.add_cog(Looting(bot))
    bot.add_cog(Games(bot))
