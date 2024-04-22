import os
import platform
import random
import discord
import logging
import psutil
import json
from discord import app_commands
from discord.ext import commands, tasks
from math import floor
from utils.util7tv import get7tvEmoteList

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


class Util(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        logger.info('Util cog loaded!')

    @tasks.loop(seconds=30)
    async def change_status(self):
        statusType = random.randint(0, 5)
        match statusType:
            case 0:
                await self.bot.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.watching,
                                              name=f'some anime'))
            case 1:
                await self.bot.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.listening,
                                              name=f'the rain outside'))
            case 2:
                await self.bot.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.watching,
                                              name=f'vtubers'))
            case 3:
                await self.bot.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.watching,
                                              name=f'smol crimes'))
            case 4:
                await self.bot.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.watching,
                                              name=f'snow fall down'))
            case 5:
                await self.bot.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.playing,
                                              name=f'games'))

    @app_commands.command(name='ping', description='Checks the bot latency')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f'Pong! Response is at a blazing fast {round(self.bot.latency * 1000)}ms',
            ephemeral=True)

    @app_commands.command(name='status', description='Status of the bot')
    async def status(self, interaction: discord.Interaction):
        process = psutil.Process(os.getpid())

        embed = discord.Embed(
            title=f'{self.bot.user.name} Status', color=discord.Color.blurple())
        embed.set_thumbnail(url=self.bot.user.display_avatar)
        embed.add_field(name='Server CPU Usage',
                        value=f'{psutil.cpu_percent()}%',
                        inline=False)
        embed.add_field(name='Server Memory Usage',
                        value=f'{psutil.virtual_memory().percent}%',
                        inline=False)
        embed.add_field(name='Process CPU Usage',
                        value=f'{process.cpu_percent()}%',
                        inline=False)
        embed.add_field(name='Process Memory Usage',
                        value=f'{floor(process.memory_info().rss / 1000 / 1000)}MB',
                        inline=False)
        embed.add_field(name='Python Version',
                        value=f'{platform.python_version()}',
                        inline=False)
        embed.add_field(name='Discord.py Version',
                        value=f'{discord.__version__}',
                        inline=False)
        embed.add_field(name='Bot latency',
                        value=f'{round(self.bot.latency * 1000)}ms',
                        inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name='avatar', description='Get a users avatar image')
    async def avatar(self, interaction: discord.Interaction, member: discord.Member):
        avatar = member.display_avatar
        await interaction.response.send_message(f"Here's your [avatar!]({avatar})",
                                                ephemeral=True)

    @app_commands.command(name='banner', description='Get a users banner image')
    async def banner(self, interaction: discord.Interaction, member: discord.Member):
        user = await self.bot.fetch_user(member.id)
        banner = user.banner.url
        await interaction.response.send_message(f"Here's your [banner!]({banner})",
                                                ephemeral=True)

    @banner.error
    async def banner_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        logger.error(f"An error occurred while fetching the banner: {error}")
        await interaction.response.send_message(
            f"This command failed! Try making sure you have a banner (you need regular nitro for this, not basic)",
            ephemeral=True)

    @app_commands.command(name='import7tv', description='Imports emotes from 7tv')
    async def import7tv(self, interaction: discord.Interaction, emote_set: str):
        logger.info(f'Attempting to import {emote_set} from 7tv!')
        emote_limit = interaction.guild.emoji_limit
        guild_emotes = interaction.guild.emojis
        emote_set = emote_set.split('/')[-1]
        data = await get7tvEmoteList(emote_set)
        emotes7tv = []
        if data:
            for emote in data['emotes']:
                emotes7tv.append([emote['name']])

            free_slots = emote_limit - len(guild_emotes)

            if free_slots > len(emotes7tv):
                logger.info(f"{free_slots} available for import, continuing...")
                await interaction.response.send_message(f'You have {free_slots} emote slots available!',)
            else:
                logger.error(f"{len(emotes7tv) - emote_limit} more emote slots needed!")
                await interaction.response.send_message(f"You need to have {len(emotes7tv) - emote_limit} more emote slots available!")

        else:
            logger.error(f'Could not find any emotes in 7tv!')
            await interaction.response.send_message(f"Couldn't find the emotes in 7tv!"
                                                    f"Please check if the link you sent is correct and try again.")


async def setup(bot):
    await bot.add_cog(Util(bot), guilds=[discord.Object(id=1116469018019233812)])
