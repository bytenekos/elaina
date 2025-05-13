import random
import discord
import logging
import aiohttp
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


def ballchoice():
    randomchoice = ["it is certain.",
                    "it is decidedly so.",
                    "without a doubt.",
                    "yes, definitely.",
                    "you may rely on it.",
                    "as I see it, yes.",
                    "most likely.",
                    "outlook good.",
                    "yes.",
                    "signs point to yes.",
                    "reply hazy, try again.",
                    "ask again later.",
                    "I better not tell you now.",
                    "I cannot predict now.",
                    "concentrate and ask again.",
                    "don't count on it.",
                    "no.",
                    "my sources say no.",
                    "outlook not so good.",
                    "very doubtful"]
    return random.choice(randomchoice)


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Fun cog loaded!')

    @app_commands.command(name="8ball", description="Put all your faith in the 8 ball!")
    async def eightball(self, interaction: discord.Interaction, *, question: str):
        s = question
        if s.endswith('?'):
            s = s[:-1]
        await interaction.response.send_message(f"Question: {s}?\n\n"
                                                f"Well, my answer is {ballchoice()}")

    @app_commands.command(name="xkcd", description="Sends an XKCD comic!")
    async def xkcd(self, interaction: discord.Interaction, comic: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://xkcd.com/{comic}') as resp:
                if resp.status == 200:
                    await interaction.response.send_message(f"https://xkcd.com/{comic}/")
                elif resp.status == 404:
                    await interaction.response.send_message(f"Comic {comic} not found!", ephemeral=True)
                else:
                    await interaction.response.send_message(f"Command failed! Reason: {resp.status}: {resp.reason}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Fun(bot), guilds=[discord.Object(id=1369464877210406942)])
