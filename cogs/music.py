import disnake
from disnake.ext import commands, tasks
import yt_dlp as youtube_dl
import asyncio

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': False,
}
FFMPEG_OPTIONS = {'options': '-vn'}

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}
        self.auto_disconnect.start()
    
    def check_queue(self, ctx):
        if ctx.guild.id in self.queues and self.queues[ctx.guild.id]:
            source = self.queues[ctx.guild.id].pop(0)
            ctx.voice_client.play(source, after=lambda e: self.check_queue(ctx))
    
    @commands.slash_command(name="play", description="Play music from YouTube")
    async def play(self, interaction: disnake.ApplicationCommandInteraction, url: str):
        await interaction.response.defer()  # Затримка

        vc = interaction.guild.voice_client
        if not vc:
            if interaction.author.voice:
                channel = interaction.author.voice.channel
                vc = await channel.connect()
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    audio_url = info['url']
            else:
                await interaction.followup.send("❌ Сначало зайдите в гс")
                return

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))
        song = data['url']
        source = disnake.FFmpegPCMAudio(song, **FFMPEG_OPTIONS)

        if vc.is_playing():
            if interaction.guild.id not in self.queues:
                self.queues[interaction.guild.id] = []
            self.queues[interaction.guild.id].append(source)
            await interaction.followup.send("🎵 Добавленно в очердь")
        else:
            vc.play(source, after=lambda e: self.check_queue(interaction))
            await interaction.followup.send("🎶 Играет музыка")
    
    # Якщо бот 1 хв в гс сам то виходим
    @tasks.loop(seconds=60)
    async def auto_disconnect(self):
        for guild in self.bot.guilds:
            vc = guild.voice_client
            if vc and len(vc.channel.members) == 1:
                await vc.disconnect()
    
    @auto_disconnect.before_loop
    async def before_auto_disconnect(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Music(bot))