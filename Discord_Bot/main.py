import discord
from discord.ext import commands
from dotenv import load_dotenv
from server import webhookReceiver
from oauth2client.service_account import ServiceAccountCredentials
from cmds.sessionGenerator import *
import gspread
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
client = commands.Bot(command_prefix = '/', intents = intents)

#initalise the database connection and clear previous sessions
scope = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name("disc-compress-cred.json", scope)
dbclient = gspread.authorize(creds)
database = dbclient.open("Disc_Compress_Requests").sheet1
if database.row_count > 1:
    database.delete_rows(2, database.row_count)
        
# Event: client is ready
@client.event
async def on_ready():
     
    await client.add_cog(commandGog(client = client, database = database))

    try: 
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

    webhookReceiver.init_webhook_reciever(client, database = database)
    print(f"The {client.user.name} is ready to compress")

@client.tree.command(name="awake")
async def awake(ctx):
    await ctx.response.send_message("I am awake and ready to compress your videos!")

@client.tree.command(name="request")
async def request(ctx):
    userID = ctx.user.id
        
    if user_exists(userID,database) and not user_exists_but_inactive(userID,database):
            await ctx.response.send_message("You already have an active session.")
            return
        
    session_code = create_session(userID, database)
        
    await ctx.response.send_message(f"Session created! Your session code is: **{session_code}**\nInput code at this website to upload your video: {os.getenv('WEBSITE_URL')}")


if __name__ == "__main__":
    
    # Run the client (Leave this at the end of the file)
    client.run(token)