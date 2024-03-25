import asyncio
import discord
import os
import logging
import time
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

print("Launching...")
time.sleep(1)
print(r"          _____                    _____            _____                    _____                    _____                    _____                  ")
print(r"         /\    \                  /\    \          /\    \                  /\    \                  /\    \                  /\    \                 ")
print(r"        /::\    \                /::\____\        /::\    \                /::\    \                /::\____\                /::\    \                ")
time.sleep(0.3)
print(r"       /::::\    \              /:::/    /       /::::\    \               \:::\    \              /::::|   |               /::::\    \               ")
print(r"      /::::::\    \            /:::/    /       /::::::\    \               \:::\    \            /:::::|   |              /::::::\    \              ")
print(r"     /:::/\:::\    \          /:::/    /       /:::/\:::\    \               \:::\    \          /::::::|   |             /:::/\:::\    \             ")
time.sleep(0.3)
print(r"    /:::/__\:::\    \        /:::/    /       /:::/__\:::\    \               \:::\    \        /:::/|::|   |            /:::/__\:::\    \            ")
print(r"   /::::\   \:::\    \      /:::/    /       /::::\   \:::\    \              /::::\    \      /:::/ |::|   |           /::::\   \:::\    \           ")
print(r"  /::::::\   \:::\    \    /:::/    /       /::::::\   \:::\    \    ____    /::::::\    \    /:::/  |::|   | _____    /::::::\   \:::\    \          ")
time.sleep(0.3)
print(r" /:::/\:::\   \:::\    \  /:::/    /       /:::/\:::\   \:::\    \  /\   \  /:::/\:::\    \  /:::/   |::|   |/\    \  /:::/\:::\   \:::\    \         ")
print(r"/:::/__\:::\   \:::\____\/:::/____/       /:::/  \:::\   \:::\____\/::\   \/:::/  \:::\____\/:: /    |::|   /::\____\/:::/  \:::\   \:::\____\        ")
print(r"\:::\   \:::\   \::/    /\:::\    \       \::/    \:::\  /:::/    /\:::\  /:::/    \::/    /\::/    /|::|  /:::/    /\::/    \:::\  /:::/    /        ")
time.sleep(0.3)
print(r" \:::\   \:::\   \/____/  \:::\    \       \/____/ \:::\/:::/    /  \:::\/:::/    / \/____/  \/____/ |::| /:::/    /  \/____/ \:::\/:::/    /         ")
print(r"  \:::\   \:::\    \       \:::\    \               \::::::/    /    \::::::/    /                   |::|/:::/    /            \::::::/    /          ")
print(r"   \:::\   \:::\____\       \:::\    \               \::::/    /      \::::/____/                    |::::::/    /              \::::/    /           ")
time.sleep(0.3)
print(r"    \:::\   \::/    /        \:::\    \              /:::/    /        \:::\    \                    |:::::/    /               /:::/    /            ")
print(r"     \:::\   \/____/          \:::\    \            /:::/    /          \:::\    \                   |::::/    /               /:::/    /             ")
print(r"      \:::\    \               \:::\    \          /:::/    /            \:::\    \                  /:::/    /               /:::/    /              ")
time.sleep(0.3)
print(r"       \:::\____\               \:::\____\        /:::/    /              \:::\____\                /:::/    /               /:::/    /               ")
print(r"        \::/    /                \::/    /        \::/    /                \::/    /                \::/    /                \::/    /                ")
print(r"         \/____/                  \/____/          \/____/                  \/____/                  \/____/                  \/____/                 ")


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
                    filename=log_file_path)

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
    bot.tree.copy_global_to(guild=MY_GUILD)
    await bot.tree.sync(guild=MY_GUILD)
    logger.info(f'Logged in as {bot.user}')
    print("Bot ready and loaded!")


@bot.tree.command(name='sync', description='syncs commands from cogs')
@app_commands.checks.has_role(1120840113170157599)
async def sync(interaction: discord.Interaction):
    fmt = await bot.tree.sync(guild=MY_GUILD)
    await interaction.response.send_message(f"Refreshed {len(fmt)} commands.", ephemeral=True)
    logger.info(f'Synced commands: {fmt}')


@sync.error
async def on_sync_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message(f"Sync command failed: {error}", ephemeral=True)
        logger.error(f"Sync command failed: {error}")


@bot.tree.command(name='loaded', description='Checks what cogs are loaded')
@app_commands.checks.has_role(1120840113170157599)
async def loaded(interaction: discord.Interaction):
    loadedresponse = '\n'.join(loadedCogs)
    await interaction.response.send_message(f"# Cogs loaded:\n{loadedresponse}", ephemeral=True)
    logger.info(f'Loaded cogs: {loadedCogs}')


@loaded.error
async def on_sync_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message(f"Loaded command failed: {error}", ephemeral=True)
        logger.error(f"Loaded command failed: {error}")


@bot.tree.command(name='unload', description='unloads a cog')
@app_commands.checks.has_role(1120840113170157599)
async def unload(interaction: discord.Interaction, cog: str):
    await bot.unload_extension(f"cogs.{cog}")
    loadedCogs.remove(cog)
    await interaction.response.send_message(f"Unloaded {cog}", ephemeral=True)
    logger.info(f'Unloaded cogs: {cog}')


@unload.error
async def on_sync_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message(f"Unload command failed: {error}", ephemeral=True)
        logger.error(f"Unload command failed: {error}")


@bot.tree.command(name='load', description='Loads a cog')
@app_commands.checks.has_role(1120840113170157599)
async def load(interaction: discord.Interaction, cog: str):
    for file in os.listdir('./cogs'):
        if file.startswith(cog):
            loadedCogs.append(file[:-3])
            await bot.load_extension(f'cogs.{file[:-3]}')
            await interaction.response.send_message(f"Loaded {cog}", ephemeral=True)
            logger.info(f"Loaded cogs: {cog}")


@load.error
async def on_sync_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message(f"Load command failed: {error}", ephemeral=True)
        logger.error(f"Load command failed: {error}")


@bot.tree.command(name='reload', description='Reloads a cog')
@app_commands.checks.has_role(1120840113170157599)
async def reload(interaction: discord.Interaction, cog: str):
    await bot.reload_extension(f"cogs.{cog}")
    await interaction.response.send_message(f"Reloaded {cog}!", ephemeral=True)
    logger.info(f"Reloaded cogs: {cog}")


@reload.error
async def on_sync_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message(f"Reload command failed: {error}", ephemeral=True)
        logger.error(f"Reload command failed: {error}")


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
