import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(".env")

intents = discord.Intents.default()
intents.message_content = True

# paste guild ID here
GUILD_ID = 12345678

bot = commands.Bot(command_prefix="?", intents=intents)

bot.lavalink_nodes = [
    {"host": "lavalink.oops.wtf", "port": 2000, "password": "www.freelavalink.ga"},
    # Can have multiple nodes here
]

# If you want to use spotify search
bot.spotify_credentials = {
    "client_id": "CLIENT_ID_HERE",
    "client_secret": "CLIENT_SECRET_HERE",
}

# If you want the slash commands to be prefixed with "music" set to True
bot.music_prefixed = True


@bot.event
async def on_ready():
    print(f"{bot.user} is ready")
    MY_GUILD = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=MY_GUILD)
    await bot.tree.sync(guild=MY_GUILD)


@bot.tree.command(name="ping", description="Pong")
async def ping_command(interaction: discord.Interaction):
    await interaction.response.send_message(embed=discord.Embed(title="Pong!"))


bot.load_extension("dismusic-slash")
bot.run(os.getenv("TOKEN"))
