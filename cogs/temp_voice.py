import disnake
from disnake.ext import commands
import asyncio

VOICE_CHANNEL_ID = 1292465088644517921
CATEGORY_ID = 1292464513232142447

class TempVoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temporary_channels = {}

    # Тимчасовий войс
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Якщо чел приєднався до войсу створення
        if after.channel and after.channel.id == VOICE_CHANNEL_ID:
            category = disnake.utils.get(member.guild.categories, id = CATEGORY_ID)
            if category:
                # Створюємо тимчасовий войс
                channel_name = f"Канал [{member.display_name}]"
                temp_channel = await category.create_voice_channel(name = channel_name)
                self.temporary_channels[temp_channel.id] = temp_channel # Записуєм войс в словник

                # Даємо челу права в войсі
                await temp_channel.set_permissions(member, 
                    manage_channels = True,
                    manage_permissions = True,
                    move_members = True
                )

                await temp_channel.set_permissions(member.guild.default_role, send_messages=False, mention_everyone=False)
                await temp_channel.set_permissions(member.guild.me, mention_everyone=False)
   
                # Переміщуємо чела в войс
                if member.voice and member.voice.channel and member.voice.channel.id == VOICE_CHANNEL_ID:
                    try:
                        await member.move_to(temp_channel)
                    except disnake.HTTPException as e:
                        # Видаляєм канал якщо чел встиг вийти до переміщення
                        await temp_channel.delete()
                        del self.temporary_channels[temp_channel.id]
                        return

                await asyncio.sleep(1)
                if len(temp_channel.members) == 0:
                    await temp_channel.delete()
                    del self.temporary_channels[temp_channel.id]
        
        # Якщо чел вийшов з тимчасового войса
        if before.channel and before.channel.id in self.temporary_channels:
            temp_channel = self.temporary_channels[before.channel.id]
            # Видаляємо тимчасовий канал, якщо в ньому нікого немає
            if len(temp_channel.members) == 0:
                await temp_channel.delete()
                del self.temporary_channels[before.channel.id]

def setup(bot):
    bot.add_cog(TempVoice(bot))