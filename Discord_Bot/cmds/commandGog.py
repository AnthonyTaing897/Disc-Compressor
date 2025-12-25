from cmds.sessionGenerator import gen_sessCode, gen_sessID
from discord.ext import commands
import gspread
from pathlib import Path
from datetime import datetime
from server.func.Alter_Video_Function import alterVideo
from server.func.Compress_Video_Function import compressVid

class commandGog(commands.Cog):
    def __init__(self, client, database : gspread.Worksheet = None):

        self.client = client
        self.database = database

        # Clear and create Temp_Videos and Processed_Videos directories
        self.temp_dir = Path(__file__).parent / "Library/Temp_Videos"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        self.processed_dir = Path(__file__).parent / "Library/Processed_Videos"
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        

    @commands.command()
    async def awake(self, ctx):
        await ctx.send("I am awake and ready to compress your videos!")

        # Message discord user when given username in plain text (Test command)
    @commands.command()
    async def MsgUser(self, ctx):
        user = ctx.message.content[9:].strip()
        print(int(user))
        targetUser = await self.client.fetch_user(int(user)) # Try to get user by ID first
        print(targetUser)
        if targetUser:
            await targetUser.send(f"Hello {targetUser.mention}! This is a message from a test bot.")
        else:
            await ctx.send(f"User '{user}' not found in this server.")

    
        # Get Discord ID of mentioned user (Test command)
    @commands.command()
    async def getId(self, ctx):
        await ctx.send(f"Your Discord ID is: {ctx.author.id}")

    @commands.command()
    async def request(self, ctx):
        userID = ctx.author.id
        
        if self.user_exists(userID,self.database):
            await ctx.send("You already have an active session.")
            return
        
        session_ID = gen_sessID(database=self.database)
        session_code = gen_sessCode(database=self.database)

        # Store session in the database sets date and time automatically
        self.database.append_row([session_ID, session_code, str(userID)])
        
        await ctx.send(f"Session created! Your session code is: {session_code}")


    def user_exists(self, userID:str, database:gspread.Worksheet) -> bool:
        records = database.get_all_records()
        for record in records:
            if str(record['User ID']) == str(userID):
                return True
        return False