import discord
from discord.ext import commands

class commandGog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def awake(self, ctx):
        await ctx.send("I am awake and ready to compress your videos!")

    # compressVid command to compress video attachments
    @commands.command()
    async def compressVid(self, ctx):
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            if attachment.content_type and attachment.content_type.startswith('video/'):
                await ctx.send("Compressing video...")
                await ctx.send(attachment)
            else:
                await ctx.send("The attachment is not a video.")

    # Joke command to send back a heavy edited video (Will remove later)
    @commands.command()
    async def editHeavy(self, ctx):
        file = discord.File("output.mp4")
        await ctx.send(file = file)