import disnake
from disnake.ext import commands
from datetime import timedelta
from error_handler import error_handler

class WarnSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {} # словник варнів

    # Команда /warn
    @commands.slash_command(name="warn", description="Warn management system")
    async def warn(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    # Підкоманда /warn add
    @warn.sub_command(name="add", description="Add a warning to a user")
    @commands.has_permissions(administrator=True)
    async def warn_add(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member):
        guild_id = interaction.guild.id
        user_id = member.id

        # Перевірка чи є чел у словнику з варном
        if guild_id not in self.warnings:
            self.warnings[guild_id] = {}
        
        if user_id not in self.warnings[guild_id]:
            self.warnings[guild_id][user_id] = 0

        # Добавляєм в словник чела
        self.warnings[guild_id][user_id] += 1
        warning_count = self.warnings[guild_id][user_id]

        await interaction.response.send_message(f"{member.mention} получил варн. Всего варнов: {warning_count}")

        # Варн на 30 хвилин
        if warning_count >= 3:
            try:
                time_duration = timedelta(minutes=30)
                await member.timeout(duration=time_duration)
                await interaction.channel.send(f"{member.mention} получил тайм-аут на 30 минут")
                self.warnings[guild_id][user_id] = 0  # Очищуємо варни
            except Exception as e:
                print(f"Error: {e}")

    # Підкоманда /warn check
    @warn.sub_command(name="check", description="Check warnings of a user")
    async def warn_check(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member):
        guild_id = interaction.guild.id
        user_id = member.id

        # Перевіряємо кількість варнів у чела
        if guild_id in self.warnings and user_id in self.warnings[guild_id]:
            warning_count = self.warnings[guild_id][user_id]
        else:
            warning_count = 0

        await interaction.response.send_message(f"В {member.mention} {warning_count} варнов")
    
    # Підкоманда /warn clear
    @warn.sub_command(name="clear", description="Clear warnings for a user")
    @commands.has_permissions(administrator=True)
    async def warn_clear(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member):
        guild_id = interaction.guild.id
        user_id = member.id

        # Перевірка чи є чел у словнику з варнами
        if guild_id in self.warnings and user_id in self.warnings[guild_id]:
            self.warnings[guild_id][user_id] = 0
            await interaction.response.send_message(f"Варны {member.mention} были очищенны")
        else:
            await interaction.response.send_message(f"В {member.mention} нету варнов для очищения", ephemeral=True)
    
    # Обробка помилок
    @warn_add.error
    async def warn_add_error(self, interaction: disnake.ApplicationCommandInteraction, error):
        await error_handler(interaction, error)

    @warn_check.error
    async def warn_check_error(self, interaction: disnake.ApplicationCommandInteraction, error):
        await error_handler(interaction, error)

    @warn_clear.error
    async def warn_clear_error(self, interaction: disnake.ApplicationCommandInteraction, error):
        await error_handler(interaction, error)

def setup(bot):
    bot.add_cog(WarnSystem(bot))