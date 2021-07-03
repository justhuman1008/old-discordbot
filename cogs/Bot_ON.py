import discord #pip
from discord.ext import commands, tasks

class Bot_ON(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command()
    async def ping(self,ctx):
        await ctx.send('pong')


def setup(client):
    client.add_cog(Bot_ON(client))