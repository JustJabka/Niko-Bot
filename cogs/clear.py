import disnake
from disnake.ext import commands
from error_handler import error_handler

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="clear",description="Clear messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, interaction: disnake.ApplicationCommandInteraction, amount: int):
        await interaction.response.send_message(f"Удалено {amount} сообщений🥞")
        await interaction.channel.purge(limit = amount + 1)
    
    @clear.error
    async def clear_error(self, interaction: disnake.ApplicationCommandInteraction, error):
        await error_handler(interaction, error)

def setup(bot):
    bot.add_cog(Clear(bot))