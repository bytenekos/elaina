import discord
from discord import app_commands, Interaction
from discord.ext import commands


def role_required(role_name: str):
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.guild:
            return False

        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if role in interaction.user.roles:
            return True
        await interaction.response.send_message("You do not have the required role to use this command.",
                                                ephemeral=True)
        return False

    return app_commands.check(predicate)
