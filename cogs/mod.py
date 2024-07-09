import discord
import logging
from discord import app_commands, Interaction
from discord.ext import commands

logger = logging.getLogger('__name__')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(filename)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


def role_required(role_name: str):
    async def predicate(interaction: discord.Interaction) -> bool:
        logger.info(f'Checking role for user {interaction.user}')
        if not interaction.guild:
            logger.warning('No guild found in interaction.')
            return False

        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if role in interaction.user.roles:
            logger.info(f'User {interaction.user} has the required role: {role_name}')
            return True
        await interaction.response.send_message("You do not have the required role to use this command.", ephemeral=True)
        logger.warning(f'User {interaction.user} does not have the required role: {role_name}')
        return False

    return app_commands.check(predicate)


class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Mod cog loaded!")

    @app_commands.command(name="ban", description="Bans a user")
    @role_required("Mods")
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "None given"):
        await member.ban(reason=reason)
        embed = discord.Embed(
            title=f"Member banned!", color=discord.Color.blurple())
        embed.set_thumbnail(url=member.display_avatar)
        embed.add_field(name="Member", value=f"<@!{member.id}>")
        embed.add_field(name="Performed by", value=f"<@!{interaction.user.id}>")
        embed.add_field(name="Reason", value=reason)

        myguild = self.bot.get_guild(1116469018019233812)
        modlog = myguild.get_channel(1178849788440092683)
        await modlog.send(embed=embed)

        await interaction.response.send_message(f"Done! Banned {member}", ephemeral=True)
        logger.info(f"Banned {member}")

    @ban.error
    async def on_ban_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(f"Ban command failed: {error}", ephemeral=True)
            logger.warning(f"Ban command failed: {error}")

    @app_commands.command(name="kick", description="Kicks a user")
    @role_required("Mods")
    @app_commands.default_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "None given"):
        await member.kick(reason=reason)
        embed = discord.Embed(
            title=f"Member kicked!", color=discord.Color.blurple())
        embed.set_thumbnail(url=member.display_avatar)
        embed.add_field(name="Member", value=f"<@!{member.id}>")
        embed.add_field(name="Performed by", value=f"<@!{interaction.user.id}>")
        embed.add_field(name="Reason", value=reason)

        myguild = self.bot.get_guild(1116469018019233812)
        modlog = myguild.get_channel(1178849788440092683)
        await modlog.send(embed=embed)

        await interaction.response.send_message(f"Done! Kicked {member}", ephemeral=True)
        logging.info(f"Kicked {member}")

    @kick.error
    async def on_kick_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(f"Kick command failed: {error}", ephemeral=True)
            logger.error(f"Kick command failed: {error}")

    @app_commands.command(name="purge", description="purge command")
    @role_required("Mods")
    @app_commands.default_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int = 100):
        await interaction.response.send_message(f"Deleting {amount} messages!", ephemeral=True)
        await interaction.channel.purge(limit=amount, bulk=True)
        await interaction.channel.send("*Messages went poof*", delete_after=1)

    @purge.error
    async def on_purge_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(f"Purge command failed: {error}", ephemeral=True)
            logger.error(f"Purge command failed: {error}")


async def setup(bot):
    await bot.add_cog(Mod(bot), guilds=[discord.Object(id=1116469018019233812)])
