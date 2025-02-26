import disnake
from disnake.ext import commands
from error_handler import error_handler

ROLE_ID = 1291795325618491403 # Роль в пінгу і яка може закрити гілку
FORUM_CHANNEL_ID = 1291795094025801858 # Гілка допомоги
TAG_ID = 1291831807926341693 # Тег [РЕШЕНО]


class Solve(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Пінг в свіжій гілці
    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if thread.parent_id == FORUM_CHANNEL_ID:
            role = thread.guild.get_role(ROLE_ID)
            if role:
                await thread.send(f"Если ваш вопрос был решён, введите команду ```/resolved```\nПользователи с ролью {role.mention} также могут закрыть ветку")

    # Команда /resolved
    @commands.slash_command(name = "resolved",description = "Solve guild")
    async def resolved(self, interaction: disnake.ApplicationCommandInteraction):
        # Якщо неправильний канал
        if not isinstance(interaction.channel, disnake.Thread):
            await interaction.response.send_message(f"Эта команда может быть запущена только в ветках https://discord.com/channels/1290213702301126688/{FORUM_CHANNEL_ID} 🍽️", ephemeral=True)
            return

        thread = interaction.channel
        author_id = thread.owner_id
        tag_to_add = None

        # Перевіряємо, чи чел має роль або є автором гілки
        if ROLE_ID not in [role.id for role in interaction.author.roles] and interaction.author.id != author_id:
            await interaction.response.send_message("У вас нет прав для использования этой команды🍽️", ephemeral=True)
            return

        try:
            if thread.parent.id == FORUM_CHANNEL_ID:
                # Якщо гілка вже закрита
                if "[РЕШЕНО✅]" in thread.name:
                    await interaction.response.send_message("Эту ветку уже закрыто🍽️")
                    return
                
                # Якщо довбохряк написав питання в назві гілки
                if len(thread.name) > 89:
                    new_thread_name = thread.name[:89]
                else:
                    new_thread_name = thread.name

                # Якщо гілка не закрита
                for tag in thread.parent.available_tags:
                    if tag.id == TAG_ID:
                        tag_to_add = tag
                        break
                
                if tag_to_add:
                    await interaction.response.send_message("Эту ветку закрыто🥞")
                    await thread.edit(name=f"[РЕШЕНО✅] {new_thread_name}", applied_tags = [tag_to_add], archived = True, locked = True)
                else:
                    await interaction.response.send_message("Не удалось найти указанный тег🍽️", ephemeral=True)
        except Exception as e:
            print(f"Error: {e}")

    # Обробка помилок
    @resolved.error
    async def resolved_error(self, interaction: disnake.ApplicationCommandInteraction, error):
        await error_handler(interaction, error)

def setup(bot):
    bot.add_cog(Solve(bot))