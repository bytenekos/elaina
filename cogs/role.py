import discord
import logging
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


class Role(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'Roles cog loaded!')

    class TestButton(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, custom_id="accept")
        async def accept(self, interaction: discord.Interaction, Button: discord.ui.Button):
            await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=1179400425510809711))
            await interaction.response.send_message(content="works", ephemeral=True)

    @app_commands.command(name="testaccept", description="test")
    async def testaccept(self, interaction: discord.Interaction):
        await interaction.response.send_message(content="accepted", view=self.TestButton())


async def setup(bot):
    await bot.add_cog(Role(bot), guilds=[discord.Object(id=1116469018019233812)])
