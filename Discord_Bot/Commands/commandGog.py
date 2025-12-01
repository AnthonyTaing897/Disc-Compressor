import discord
from discord.ext import commands
from Alter_Video_Function import alterVideo
from pathlib import Path
import os

class commandGog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Clear and create Temp_Videos and Processed_Videos directories
        self.temp_dir = Path(__file__).parent / "Temp_Videos"
        os.remove(self.temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        self.processed_dir = Path(__file__).parent / "Processed_Videos"
        os.remove(self.processed_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        

    @commands.command()
    async def awake(self, ctx):
        await ctx.send("I am awake and ready to compress your videos!")

    # compressVid command to compress video attachments (Not functional yet)
    @commands.command()
    async def compressVid(self, ctx):
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            if attachment.content_type and attachment.content_type.startswith('video/'):
                await ctx.send("Compressing video...")
                await ctx.send(attachment)
            else:
                await ctx.send("The attachment is not a video.")

    # Joke command to send back an edited video (Will remove later)
    @commands.command()
    async def alterVideo(self, ctx):
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            if attachment.content_type and attachment.content_type.startswith('video/'):
                await ctx.send("Altering video...")
                
                temp_save_path = self.temp_dir / attachment.filename

                # save attachment into Temp_Videos
                await attachment.save(fp = temp_save_path, use_cached=False)

                proccess_save_path = alterVideo(temp_save_path,self.processed_dir,attachment.filename)
                file = discord.File(proccess_save_path)
                
                
                await ctx.send(file=file)
                await ctx.send("Video altered successfully!")

                os.remove(temp_save_path)
                os.remove(proccess_save_path)
            else:
                await ctx.send("The attachment is not a video.")
        else:
            await ctx.send("No attachment found.")

    # alterVideo Command to save video to Temp_Videos folder
    @commands.command()
    async def saveVideo(self, ctx):
        await ctx.send("Saving video...")
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            if attachment.content_type and attachment.content_type.startswith('video/'):
                save_path = self.temp_dir / attachment.filename

                # save attachment into Temp_Videos
                await attachment.save(fp = save_path, use_cached=False)
                await ctx.send("Saved video successfully!")
            else:
                await ctx.send("The attachment is not a video.")