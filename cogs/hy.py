import discord #pip
from discord.ext import commands, tasks
import random






class hy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['하픽', '하이픽셀'])
    async def _hyhelp(self, ctx):
        embed = discord.Embed(title="해당 명령어는 준비중입니다.", description="`준비중`", color=0xffdc16)
        await ctx.send(embed = embed)





def setup(client):
    client.add_cog(hy(client))