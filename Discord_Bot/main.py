import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load command list cog
from Commands.commandGog import commandGog


load_dotenv()
# Bot Token
token = os.getenv('DISCORD_TOKEN')
if not token:
    raise EnvironmentError('DISCORD_TOKEN not set in environment')


# Bot Intent
intents = discord.Intents.default()
intents.message_content = True

# Set up Command Prefix and Intents
bot = commands.Bot(command_prefix = '%', intents = intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    await bot.add_cog(commandGog(bot))
    print(f"The {bot.user.name} is ready to compress")

# Run the bot (Leave this at the end of the file)
bot.run(token)