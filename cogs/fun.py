import random
import discord
import logging
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Fun cog loaded!')

    @app_commands.command(name="8ball", description="Put all your faith in the 8 ball!")
    async def eightball(self, interaction: discord.Interaction, *, question: str):
        ballchoice = random.randint(1, 20)
        match ballchoice:
            case 1:
                await interaction.response.send_message("It is certain.", ephemeral=True)
            case 2:
                await interaction.response.send_message("It is decidedly so.", ephemeral=True)
            case 3:
                await interaction.response.send_message("Without a doubt.", ephemeral=True)
            case 4:
                await interaction.response.send_message("Yes definitely.", ephemeral=True)
            case 5:
                await interaction.response.send_message("You may rely on it.", ephemeral=True)
            case 6:
                await interaction.response.send_message("As I see it, yes.", ephemeral=True)
            case 7:
                await interaction.response.send_message("Most likely.", ephemeral=True)
            case 8:
                await interaction.response.send_message("Outlook good.", ephemeral=True)
            case 9:
                await interaction.response.send_message("Yes.", ephemeral=True)
            case 10:
                await interaction.response.send_message("Signs point to yes.", ephemeral=True)
            case 11:
                await interaction.response.send_message("Reply hazy, try again.", ephemeral=True)
            case 12:
                await interaction.response.send_message("Ask again later.", ephemeral=True)
            case 13:
                await interaction.response.send_message("Better not tell you now.", ephemeral=True)
            case 14:
                await interaction.response.send_message("Cannot predict now.", ephemeral=True)
            case 15:
                await interaction.response.send_message("Concentrate and ask again.", ephemeral=True)
            case 16:
                await interaction.response.send_message("Don't count on it.", ephemeral=True)
            case 17:
                await interaction.response.send_message("My reply is no.", ephemeral=True)
            case 18:
                await interaction.response.send_message("My sources say no.", ephemeral=True)
            case 19:
                await interaction.response.send_message("Outlook not so good.", ephemeral=True)
            case 20:
                await interaction.response.send_message("Very doubtful.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Fun(bot), guilds=[discord.Object(id=1116469018019233812)])