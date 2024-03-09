import discord
import random
import logging
from discord.ext import commands

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'Roles cog loaded!')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        logger.info(f'Member joined: {member}')
        responses = [
            f"Lets all welcome in <@{member.id}>!",
            f"Hey look, <@{member.id}> has joined the server!",
            f"Hi there <@{member.id}>! Hope you enjoy your stay here.",
            f"Welcome to the server, <@{member.id}>!",
        ]
        myguild = self.bot.get_guild(1116469018019233812)
        welcome = myguild.get_channel(1178850385901932564)
        role = myguild.get_role(1179086276935299164)
        await member.add_roles(role)
        await welcome.send(random.choice(responses))


async def setup(bot):
    await bot.add_cog(Roles(bot), guilds=[discord.Object(id=1116469018019233812)])
