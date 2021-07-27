import discord #pip
from discord.ext import commands
import asyncio
#import pyNaCl

class voice(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['참가', '들어와', '참여'])
    async def _join(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel: # 채널에 들어가 있는지 파악
            channel = ctx.author.voice.channel # 채널 구하기
            await channel.connect() # 채널 연결
        else: # 유저가 채널에 없으면
            await ctx.send(embed=discord.Embed(title=f'음성채널에 유저가 없습니다.', description='음성 채널에 참가해주세요', color=0xf8e71c)) # 출력

    @commands.command(aliases=['나가'])
    async def _stop(self, ctx):
        await ctx.voice_client.disconnect()


def setup(client):
    client.add_cog(voice(client))