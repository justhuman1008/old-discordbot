import discord #pip
from discord.ext import commands, tasks
import time
from traceback import print_exc

class Bot_ON(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands

    @commands.command()
    async def test(self, ctx):
        await ctx.send('test')

    @commands.command()
    async def 도움(self, ctx):
        await ctx.send('도움말 준비중')




def setup(client):
    client.add_cog(Bot_ON(client))