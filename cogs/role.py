import discord
import logging
import random
from discord import app_commands
from discord.ext import commands
from utils.roleChecks import role_required

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


async def add_roles(self, interaction: discord.Interaction):
    await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=1179086276935299164))
    await interaction.response.send_message(content="You've been accepted, enjoy the server!", ephemeral=True)


class VerifyButton(discord.ui.View):
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
        await add_roles(self, interaction)
        welcomechannel = discord.utils.get(interaction.guild.channels, id=1178850385901932564)
        await welcomechannel.send(random.choice(responses))

    @discord.ui.button(label="Silent Accept", style=discord.ButtonStyle.grey, custom_id="silent_accept")
    async def silent_accept(self, interaction: discord.Interaction, Button: discord.ui.Button):
        logger.info(f'Member accepted: {interaction.user.name}, ID: {interaction.user.id}')
        await add_roles(self, interaction)


class Roles(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='Twitch',
                                 value='Twitch',
                                 description='Notifies you of when I go live on Twitch!'),
            discord.SelectOption(label='Show Off',
                                 value='Show Off',
                                 description='Notifies you when I send something in the "show off" channel!'),
            discord.SelectOption(label='Server Announcements',
                                 value='Server Announcements',
                                 description="Notifies you when there's a server announcement!")
        ]
        super().__init__(placeholder='Select your role!', min_values=1, max_values=1, options=options,
                         custom_id='rolepicker')

    async def callback(self, interaction: discord.Interaction):
        selection = self.values[0]

        match selection:
            case 'Twitch':
                await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=1179188900745457745))
            case 'Show Off':
                await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=1222310438939787274))
            case 'Server Announcements':
                await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=1222310641268953119))
        await interaction.response.send_message(f'Given role {selection}!', ephemeral=True)


class Dropdown(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Roles())


class Role(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'Roles cog loaded!')

    @app_commands.command(name="sendverify", description="sends a verification message to a channel")
    @role_required("RAT")
    @app_commands.default_permissions(administrator=True)
    async def accept(self, interaction: discord.Interaction):
        await interaction.channel.send(content="Press the button below if you've read and accept the rules!",
                                       view=VerifyButton())
        await interaction.response.send_message(content="Sent button!", ephemeral=True)

    @accept.error
    async def on_sync_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(f"Verify command failed: {error}", ephemeral=True)
            logger.error(f"Verify command failed: {error}")

    @app_commands.command(name="sendroles", description="sends a role setup message to a channel")
    @role_required("RAT")
    @app_commands.default_permissions(administrator=True)
    async def sendroles(self, interaction: discord.Interaction):
        await interaction.response.send_message("Sent!", ephemeral=True)
        await interaction.channel.send(content="Select your roles here!", view=Dropdown())

    @sendroles.error
    async def on_role_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(f"Roles command failed: {error}", ephemeral=True)
            logger.error(f"Roles command failed: {error}")


async def setup(bot):
    bot.add_view(VerifyButton())
    bot.add_view(Dropdown())
    await bot.add_cog(Role(bot), guilds=[discord.Object(id=1369464877210406942)])
