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
            return "It is certain."
        case 2:
            return "It is decidedly so."
        case 3:
            return "Without a doubt."
        case 4:
            return "Yes definitely."
        case 5:
            return "You may rely on it."
        case 6:
            return "As I see it, yes."
        case 7:
            return "Most likely."
        case 8:
            return "Outlook good."
        case 9:
            return "Yes."
        case 10:
            return "Signs point to yes."
        case 11:
            return "Reply hazy, try again."
        case 12:
            return "Ask again later."
        case 13:
            return "Better not tell you now."
        case 14:
            return "Cannot predict now."
        case 15:
            return "Concentrate and ask again."
        case 16:
            return "Don't count on it."
        case 17:
            return "My reply is no."
        case 18:
            return "My sources say no."
        case 19:
            return "Outlook not so good."
        case 20:
            return "Very doubtful"


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Fun cog loaded!')

    @app_commands.command(name="8ball", description="Put all your faith in the 8 ball!")
    async def eightball(self, interaction: discord.Interaction, *, question: str):
        await interaction.response.send_message(ballchoice())


async def setup(bot):
    await bot.add_cog(Fun(bot), guilds=[discord.Object(id=1116469018019233812)])
