import discord
from discord.ext import commands
from discord import app_commands
from utils.matchmaking import Matchmaker
import yaml

class PairingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.matchmaker = Matchmaker()
        with open("config.yaml", "r") as f:
            cfg = yaml.safe_load(f)
        self.roles = cfg['roles']

    def genders_match(self, a, b):
        # If either has no gender role => random
        a_roles = [r.id for r in a.roles]
        b_roles = [r.id for r in b.roles]
        if not self.roles['male'] or not self.roles['female']:
            return True
        male = int(self.roles['male'])
        female = int(self.roles['female'])
        # Same preference or random
        if (male not in a_roles and female not in a_roles) or \
           (male not in b_roles and female not in b_roles):
            return True
        return (male in a_roles and male in b_roles) or (female in a_roles and female in b_roles)

    async def find_partner(self, user):
        # Custom matchmaking: skip until gender_match
        for candidate in list(self.matchmaker.queue):
            if candidate != user and self.genders_match(user, candidate):
                self.matchmaker.queue.remove(candidate)
                self.matchmaker.pairs[user] = candidate
                self.matchmaker.pairs[candidate] = user
                return candidate
        return None

    @commands.command(name='start')
    async def start_pairing(self, ctx: commands.Context):
        partner = await self.matchmaker.join_queue(ctx.author, custom_match=self.find_partner)
        if partner:
            channel = await ctx.guild.create_text_channel(
                name=f"omegle-{ctx.author.id}-{partner.id}",
                overwrites={
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    ctx.author: discord.PermissionOverwrite(read_messages=True),
                    partner: discord.PermissionOverwrite(read_messages=True)
                }
            )
            await channel.send(f"Connected: {ctx.author.mention} ↔ {partner.mention}")
        else:
            await ctx.send("Waiting for a gender-matched partner...")

    @app_commands.command(name="start", description="Start a text pairing session")
    async def slash_start(self, interaction: discord.Interaction):
        partner = await self.matchmaker.join_queue(interaction.user, custom_match=self.find_partner)
        if partner:
            channel = await interaction.guild.create_text_channel(
                name=f"omegle-{interaction.user.id}-{partner.id}",
                overwrites={
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.user: discord.PermissionOverwrite(read_messages=True),
                    partner: discord.PermissionOverwrite(read_messages=True)
                }
            )
            await channel.send(f"Connected: {interaction.user.mention} ↔ {partner.mention}")
            await interaction.response.send_message("You have been connected!", ephemeral=True)
        else:
            await interaction.response.send_message("Waiting for a gender-matched partner...", ephemeral=True)

    # Stop commands unchanged (delete temp channels in stop handlers) ...