import discord
from discord.ext import commands
import yaml

# Load configuration
def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

config = load_config()
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.reactions = True

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    await bot.tree.sync(guild=discord.Object(id=config.get('guild_id')))

# Load Cogs dynamically
async def setup():
    for ext in ['cogs.roles', 'cogs.pairing', 'cogs.voice']:
        await bot.load_extension(ext)

bot.loop.create_task(setup())
bot.run(config['token'])