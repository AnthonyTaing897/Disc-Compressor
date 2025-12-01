import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
# Bot Token
token = os.getenv('DISCORD_TOKEN')
if not token:
    raise EnvironmentError('DISCORD_TOKEN not set in environment')

# Bot Intent
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '%', intents = intents)

@bot.event
async def on_ready():
    print(f"The {bot.user.name} is ready to compress")

bot.run(token)