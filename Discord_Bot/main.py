import discord
from discord.ext import commands
from dotenv import load_dotenv

import os

# Load command list cog
from cmds.commandGog import commandGog

# client Token
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
if not token:
    raise EnvironmentError('DISCORD_TOKEN not set in environment')


# client Intent
intents = discord.Intents.default()
intents.message_content = True

# Set up Command Prefix and Intents
client = commands.Bot(command_prefix = '%', intents = intents)

# Event: client is ready
@client.event
async def on_ready():
    await client.add_cog(commandGog(client))
    print(f"The {client.user.name} is ready to compress")

# Run the client (Leave this at the end of the file)
client.run(token)