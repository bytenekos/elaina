import random
import discord
import logging
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


def ballchoice():
    ballrandom = random.randint(1, 20)
    match ballrandom:
        case 1:
            return "it is certain."
        case 2:
            return "it is decidedly so."
        case 3:
            return "without a doubt."
        case 4:
            return "yes, definitely."
        case 5:
            return "you may rely on it."
        case 6:
            return "as I see it, yes."
        case 7:
            return "most likely."
        case 8:
            return "outlook good."
        case 9:
            return "yes."
        case 10:
            return "signs point to yes."
        case 11:
            return "reply hazy, try again."
        case 12:
            return "ask again later."
        case 13:
            return "I better not tell you now."
        case 14:
            return "I cannot predict now."
        case 15:
            return "concentrate and ask again."
        case 16:
            return "don't count on it."
        case 17:
            return "no."
        case 18:
            return "my sources say no."
        case 19:
            return "outlook not so good."
        case 20:
            return "very doubtful"


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
        s = s.replace("I", "you")
        s = s.replace("i", "you")
        s = s[0].lower() + s[1:]
        await interaction.response.send_message(f"You ask me, {s}?\n"
                                                f"Well, my answer is {ballchoice()}")


async def setup(bot):
    await bot.add_cog(Fun(bot), guilds=[discord.Object(id=1116469018019233812)])
