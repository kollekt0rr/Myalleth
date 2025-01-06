from .slash_commands import SlashCommands


def setup(bot):
    bot.add_cog(SlashCommands(bot))
