import discord
from discord.ext import commands

from pathlib import Path
import os

from cmds.func.Alter_Video_Function import alterVideo
from cmds.func.Compress_Video_Function import compressVid

class commandGog(commands.Cog):
    def __init__(self, client):
        self.client = client

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
    async def getId(self, ctx, target: discord.Member = None):
        if target:
            await ctx.send(f"{target.name}'s Discord ID is: {target.id}")
        else:
            await ctx.send("Please mention a user to get their Discord ID.")

    # compress command to compress video attachments
    @commands.command()
    async def compress(self, ctx):
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            if attachment.content_type and attachment.content_type.startswith('video/'):
                await ctx.send("Compressing video...")
                
                temp_save_path = self.temp_dir / attachment.filename

                # save attachment into Temp_Videos
                await attachment.save(fp = temp_save_path, use_cached=False)

                proccess_save_path = compressVid(temp_save_path,self.processed_dir,attachment.filename,3)
                file = discord.File(proccess_save_path)

                await ctx.send(file=file)
                await ctx.send("Video compressed successfully!")

                os.remove(temp_save_path)
                os.remove(proccess_save_path)

            else:
                await ctx.send("The attachment is not a video.")

    # Joke command to send back an edited video (Will remove later)
    @commands.command()
    async def alter(self, ctx):
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