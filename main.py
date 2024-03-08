import asyncio
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
loadedCogs = []
MY_GUILD = discord.Object(id=1116469018019233812)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix='!',
                   intents=intents,
                   application_id='991731064026448043',
                   guilds=[discord.Object(id=1116469018019233812)])


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


async def main():
    await bot.start(TOKEN)


asyncio.run(main())
