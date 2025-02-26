import os
import disnake
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, test_guilds=[1290213702301126688])

@bot.event
async def on_ready():
    print("Niko is ready🥞")

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

bot.run(token=TOKEN)

if __name__ == "__main__":
    bot.run_bot()