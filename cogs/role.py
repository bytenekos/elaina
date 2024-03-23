import discord
import logging
import random
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


class TestButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, custom_id="accept")
    async def accept(self, interaction: discord.Interaction, Button: discord.ui.Button):
        logger.info(f'Member accepted: {interaction.user.name}, ID: {interaction.user.id}')
        responses = [
            f"Lets all welcome in <@{interaction.user.id}>!",
            f"Hey look, <@{interaction.user.id}> has joined the server!",
            f"Hi there <@{interaction.user.id}>! Hope you enjoy your stay here.",
            f"Welcome to the server, <@{interaction.user.id}>!",
        ]
        welcomechannel = discord.utils.get(interaction.guild.channels, id=1178850385901932564)
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=1179086276935299164))
        await welcomechannel.send(random.choice(responses))
        await interaction.response.send_message(content="You've been accepted, enjoy the server!", ephemeral=True)


class Role(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'Roles cog loaded!')

    @app_commands.command(name="sendverify", description="sends a verification message to a channel")
    @app_commands.checks.has_role(1120840113170157599)
    async def accept(self, interaction: discord.Interaction):
        await interaction.channel.send(content="Press the button below if you've read and accept the rules!", view=TestButton())
        await interaction.response.send_message(content="Sent button!", ephemeral=True)

    @accept.error
    async def on_sync_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(f"Verify command failed: {error}", ephemeral=True)
            logger.error(f"Verify command failed: {error}")


async def setup(bot):
    bot.add_view(TestButton())
    await bot.add_cog(Role(bot), guilds=[discord.Object(id=1116469018019233812)])
