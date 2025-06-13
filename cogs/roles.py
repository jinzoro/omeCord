import discord
from discord.ext import commands
from discord import app_commands
import yaml

class RoleSelection(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("config.yaml", "r") as f:
            cfg = yaml.safe_load(f)
        self.roles = cfg['roles']

    @commands.command(name='setup_gender')
    @commands.has_permissions(administrator=True)
    async def setup_gender(self, ctx: commands.Context):
        """Send an embed for users to select matching gender roles."""
        embed = discord.Embed(
            title="Select Your Match Preference",
            description=(
                "React with ♂️ for Male, ♀️ for Female, or 🎲 for Random matching."
            ),
            color=discord.Color.blue()
        )
        msg = await ctx.send(embed=embed)
        for emoji in ['♂️', '♀️', '🎲']:
            await msg.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        emoji = str(reaction.emoji)
        role_id = None
        if emoji == '♂️':
            role_id = self.roles['male']
        elif emoji == '♀️':
            role_id = self.roles['female']
        elif emoji == '🎲':
            # Remove any gender roles => random
            for r in [self.roles['male'], self.roles['female']]:
                if r:
                    await user.remove_roles(discord.Object(id=r))
            return
        if role_id:
            guild = reaction.message.guild
            role = guild.get_role(int(role_id))
            if role:
                # Remove opposite if exists
                opp = self.roles['female'] if emoji == '♂️' else self.roles['male']
                if opp:
                    await user.remove_roles(discord.Object(id=opp))
                await user.add_roles(role)