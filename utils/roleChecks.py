import discord
from discord import app_commands, Interaction
from discord.ext import commands


def role_required(role_name: str):
    async def predicate(interaction: discord.Interaction) -> bool:
        # logger.info(f'Checking role for user {interaction.user}')
        if not interaction.guild:
            # logger.warning('No guild found in interaction.')
            return False

        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if role in interaction.user.roles:
            # logger.info(f'User {interaction.user} has the required role: {role_name}')
            return True
        await interaction.response.send_message("You do not have the required role to use this command.",
                                                ephemeral=True)
        # logger.warning(f'User {interaction.user} does not have the required role: {role_name}')
        return False

    return app_commands.check(predicate)
