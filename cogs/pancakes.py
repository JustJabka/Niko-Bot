from disnake.ext import commands

class Pancakes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="pancakes",description="Returns Pancakes!")
    async def pancakes(self, interaction):
        await interaction.response.send_message("Pancakes🥞")

def setup(bot):
    bot.add_cog(Pancakes(bot))