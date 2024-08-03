import os
import platform
import random
import discord
import logging
import psutil
import json
import re
import aiofiles
import sys
from discord import app_commands
from discord.ext import commands, tasks
from math import floor
from utils.util7tv import get7tvEmoteList, download7tvEmoteAnimated, download7tvEmoteNonAnimated, parseGuildEmotes, compress7tvEmote
from utils.roleChecks import role_required

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
    @role_required("Mods")
    @app_commands.default_permissions(ban_members=True)
    async def import7tv(self, interaction: discord.Interaction, emote_set: str):
        logger.info(f'Attempting to import {emote_set} from 7tv!')
        emote_limit = interaction.guild.emoji_limit
        guild_emotes = interaction.guild.emojis
        emote_set = emote_set.split('/')[-1]
        data = await get7tvEmoteList(emote_set)
        emotes7tv_animated = []
        emotes7tv_non_animated = []

        animatedID = []
        non_animatedID = []
        if data:
            for emote in data['emotes']:
                if emote['data']['animated']:
                    animatedID.append(emote['id'])
                else:
                    non_animatedID.append(emote['id'])

                animated = emote['data']['animated']
                url_parts = emote['data']['host']['url'].split('/')
                last_part = url_parts[-1]
                if animated:
                    emotes7tv_animated.append(emote['name'])
                else:
                    emotes7tv_non_animated.append(emote['name'])

            guild_parse = f"{guild_emotes}"
            animated_emotes, non_animated_emotes = await parseGuildEmotes(guild_parse)
            animated_free = emote_limit - animated_emotes
            non_animated_free = emote_limit - non_animated_emotes

            if len(emotes7tv_animated) < animated_free and len(emotes7tv_non_animated) < non_animated_free:
                logger.info(f"{animated_free} animated slots and {non_animated_free} non animated slots available for import, continuing...")
                counter_non_animated = 0
                counter_animated = 0
                await interaction.response.send_message(f'{animated_free} animated slots and {non_animated_free} non animated slots available! Attempting to add all emojis, please wait...', ephemeral=True)
                for emote_id, emote_name in zip(non_animatedID, emotes7tv_non_animated):
                    downloaded = await download7tvEmoteNonAnimated(emote_id, emote_name)
                    emotebytes = sys.getsizeof(downloaded)

                    if emotebytes > 250000:
                        emote_compressed = await compress7tvEmote(downloaded, emote_name)
                        if sys.getsizeof(emote_compressed) > 250000:
                        else:
                            await interaction.guild.create_custom_emoji(name=emote_name, image=emote_compressed, reason=None)
                            counter_non_animated += 1
                    else:
                        await interaction.guild.create_custom_emoji(name=emote_name, image=downloaded, reason=None)

                if counter_non_animated >= 0:
                    await interaction.edit_original_response(content=f'Successfully added all non animated emotes!')
                else:
                    await interaction.edit_original_response(content=f"Can't add all animated emotes!")
                for emote_id, emote_name in zip(animatedID, emotes7tv_animated):
                    downloaded = await download7tvEmoteAnimated(emote_id, emote_name)
                    emotebytes = sys.getsizeof(downloaded)
                    if emotebytes > 250000:
                        emote_compressed = await compress7tvEmote(downloaded, emote_name)
                        if sys.getsizeof(emote_compressed) > 250000:
                        else:
                            await interaction.guild.create_custom_emoji(name=emote_name, image=emote_compressed, reason=None)
                            counter_animated += 1
                    else:
                        await interaction.guild.create_custom_emoji(name=emote_name, image=downloaded, reason=None)

                if counter_animated >= 0:
                    await interaction.edit_original_response(content=f'Successfully added all animated emotes!')
                else:
                    await interaction.edit_original_response(content=f"Can't add all animated emotes!")

            elif len(emotes7tv_animated) > animated_free:
                logger.error(f"{len(emotes7tv_animated) - animated_free} more emote slots needed!")
                await interaction.response.send_message(
                    f"You need to have {len(emotes7tv_animated) - animated_free} more animated emote slots available!", ephemeral=True)

            elif len(emotes7tv_non_animated) > non_animated_free:
                logger.error(f"{len(emotes7tv_non_animated) - non_animated_free} more emote slots needed!")
                await interaction.response.send_message(
                    f"You need to have {len(emotes7tv_non_animated) - non_animated_free} more non animated emote slots available!", ephemeral=True)

            else:
                logger.error(f'Could not find any emotes in 7tv!')
                await interaction.response.send_message(f"Couldn't find the emotes in 7tv!"
                                                        f"Please check if the link you sent is correct and try again.",
                                                        ephemeral=True)


async def setup(bot):
    await bot.add_cog(Util(bot), guilds=[discord.Object(id=1116469018019233812)])
