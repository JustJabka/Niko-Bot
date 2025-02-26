import disnake
from disnake.ext import commands

async def error_handler(interaction: disnake.ApplicationCommandInteraction, error):
    if isinstance(error, commands.MissingPermissions) or isinstance(error, commands.MissingRole):
        await interaction.response.send_message("У вас нету прав для использования этой команды🍽️", ephemeral=True)