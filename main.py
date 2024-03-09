import asyncio
import discord
import os
import logging
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
MY_GUILD = discord.Object(id=1116469018019233812)
loadedCogs = []
log_folder = 'logs'
os.makedirs(log_folder, exist_ok=True)
log_file_name = f"log_date_{datetime.now().strftime('%Y-%m-%d')}_time_{datetime.now().strftime('%H-%M-%S')}.txt"
log_file_path = os.path.join(log_folder, log_file_name)

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=log_file_path,)

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


async def loadCogs():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            loadedCogs.append(file[:-3])
            await bot.load_extension(f'cogs.{file[:-3]}')
            logging.info(f'Loaded cog {file[:-3]}')


async def main():
    await loadCogs()
    await bot.start(TOKEN)


asyncio.run(main())
