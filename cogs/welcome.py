import discord
import random
import logging
from discord.ext import commands

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'Roles cog loaded!')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        logger.info(f'Member joined: {member}')


async def setup(bot):
    await bot.add_cog(Welcome(bot), guilds=[discord.Object(id=1116469018019233812)])
