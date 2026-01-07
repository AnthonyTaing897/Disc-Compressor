from cmds.sessionGenerator import *
from discord.ext import commands
import gspread
from pathlib import Path
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