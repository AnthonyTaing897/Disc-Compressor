from cmds.sessionGenerator import *
from discord.ext import commands
import gspread
from pathlib import Path
from server.func.Alter_Video_Function import alterVideo
from server.func.Compress_Video_Function import compressVid
import shutil

class commandGog(commands.Cog):
    def __init__(self, client, database : gspread.Worksheet = None):

        self.client = client
        self.database = database

        # Clear and create Temp_Videos and Processed_Videos directories
        self.temp_dir = Path(__file__).parent / "Library/Temp_Videos"
        self.processed_dir = Path(__file__).parent / "Library/Processed_Videos"
        
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        if self.processed_dir.exists():
            shutil.rmtree(self.processed_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    @commands.command()
    async def awake(self, ctx):
        await ctx.send("I am awake and ready to compress your videos!")

    @commands.command()
    async def request(self, ctx):
        userID = ctx.author.id
        
        if user_exists(userID,self.database) and not user_exists_but_inactive(userID,self.database):
            await ctx.send("You already have an active session.")
            return
        
        session_code = create_session(userID, self.database)
        
        await ctx.send(f"Session created! Your session code is: **{session_code}**")