import discord
from discord.ext import commands
from discord import app_commands
from utils.matchmaking import Matchmaker
import yaml

class VoiceCog(commands.Cog):
    """Cog for voice pairing with gender-role filtering."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.matchmaker = Matchmaker(voice=True)
        with open("config.yaml", "r") as f:
            cfg = yaml.safe_load(f)
        self.roles = cfg['roles']

    def genders_match(self, a, b):
        # same logic as PairingCog
        a_ids = [r.id for r in a.roles]
        b_ids = [r.id for r in b.roles]
        male = self.roles.get('male')
        female = self.roles.get('female')
        if not male or not female:
            return True
        male, female = int(male), int(female)
        if (male not in a_ids and female not in a_ids) or \
           (male not in b_ids and female not in b_ids):
            return True
        return (male in a_ids and male in b_ids) or (female in a_ids and female in b_ids)

    async def find_partner(self, user):
        for candidate in list(self.matchmaker.queue):
            if candidate != user and self.genders_match(user, candidate):
                self.matchmaker.queue.remove(candidate)
                self.matchmaker.pairs[user] = candidate
                self.matchmaker.pairs[candidate] = user
                return candidate
        return None

    @commands.command(name='vstart')
    async def start_voice(self, ctx: commands.Context):
        """Prefix command to start voice pairing."""
        if not ctx.author.voice:
            return await ctx.send("You need to be in a voice channel to start.")
        partner = await self.matchmaker.join_queue(ctx.author, custom_match=self.find_partner)
        if partner:
            channel = await ctx.guild.create_voice_channel(
                name=f"omegle-v-{ctx.author.id}-{partner.id}",
                overwrites={
                    ctx.guild.default_role: discord.PermissionOverwrite(connect=False),
                    ctx.author: discord.PermissionOverwrite(connect=True),
                    partner: discord.PermissionOverwrite(connect=True)
                }
            )
            await ctx.author.move_to(channel)
            await partner.move_to(channel)
        else:
            await ctx.send("Waiting for a gender-matched voice partner...")

    @app_commands.command(name="vstart", description="Start a voice pairing session")
    async def slash_vstart(self, interaction: discord.Interaction):
        """Slash command to start voice pairing."""
        if not interaction.user.voice:
            return await interaction.response.send_message("You need to be in a voice channel.", ephemeral=True)
        partner = await self.matchmaker.join_queue(interaction.user, custom_match=self.find_partner)
        if partner:
            channel = await interaction.guild.create_voice_channel(
                name=f"omegle-v-{interaction.user.id}-{partner.id}",
                overwrites={
                    interaction.guild.default_role: discord.PermissionOverwrite(connect=False),
                    interaction.user: discord.PermissionOverwrite(connect=True),
                    partner: discord.PermissionOverwrite(connect=True)
                }
            )
            await interaction.user.move_to(channel)
            await partner.move_to(channel)
            await interaction.response.send_message("Connected in voice channel!", ephemeral=True)
        else:
            await interaction.response.send_message("Waiting for a gender-matched voice partner...", ephemeral=True)

    @commands.command(name='vstop')
    async def stop_voice(self, ctx: commands.Context):
        """Leave voice pairing session and delete the temporary channel."""
        await self.matchmaker.leave_queue(ctx.author)
        voice_state = ctx.author.voice
        if voice_state and voice_state.channel.name.startswith("omegle-v-"):
            await voice_state.channel.delete()
        else:
            await ctx.send("You have left the voice queue.")

    @app_commands.command(name="vstop", description="Leave voice pairing session")
    async def slash_vstop(self, interaction: discord.Interaction):
        """Slash command to leave voice pairing session and delete the temporary channel."""
        await self.matchmaker.leave_queue(interaction.user)
        voice_state = interaction.user.voice
        if voice_state and voice_state.channel.name.startswith("omegle-v-"):
            await voice_state.channel.delete()
        else:
            await interaction.response.send_message("You have left the voice queue.", ephemeral=True)

async def setup(bot: commands.Bot):
    bot.add_cog(VoiceCog(bot))