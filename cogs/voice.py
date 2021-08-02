import discord #pip
from discord.ext import commands
import asyncio
#import pyNaCl

class voice(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['음성'])
    async def _voicehelp(self, ctx):
        embed = discord.Embed(title="음성 채널 관련 명령어", description="­", color=0xffdc16)
        embed.add_field(name=':small_blue_diamond:'+"!참가", value="유저가 참여중인 음성채널에 연결합니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!나가", value="음성채널에서 나갑니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!음소거", value="봇의 마이크를 끕니다.", inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/870547423196499968/3faa9d34cc341657.png')
        await ctx.send(embed = embed)

    @commands.command(aliases=['참가', '들어와', '참여'])
    async def _join(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel: # 채널에 들어가 있는지 파악
            channel = ctx.author.voice.channel # 채널 구하기
            if ctx.voice_client:
                await ctx.send(embed=discord.Embed(title=f'이미 봇이 음성채널에 연결되어 있습니다.', description='봇을 내보내려면 `!나가`를 입력해주세요.', color=0xf8e71c)) # 출력
            else:
                await channel.connect() # 채널 연결
                await ctx.guild.change_voice_state(channel=channel, self_deaf=True)
        else: # 유저가 채널에 없으면
            await ctx.send(embed=discord.Embed(title=f'음성채널에 유저가 없습니다.', description='음성 채널에 참가해주세요', color=0xf8e71c)) # 출력

    @commands.command(aliases=['나가'])
    async def _stop(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel # 채널 구하기
            if ctx.voice_client:
                await ctx.voice_client.disconnect()
            else:
                await ctx.send(embed=discord.Embed(title=f'봇이 음성채널에 연결되어 있지 않습니다.', color=0xf8e71c)) # 출력
        else:
            await ctx.send(embed=discord.Embed(title=f'당신은 음성채널에 연결되어 있지 않습니다.', description='음성채널에 참여한 유저만 `!나가`를 사용할 수 있습니다.', color=0xf8e71c)) # 출력

    @commands.command(aliases=['음소거'])
    async def _mute(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel # 채널 구하기
            if ctx.voice_client:
                await ctx.guild.change_voice_state(channel=channel, self_mute=True, self_deaf=True)
            else:
                await ctx.send(embed=discord.Embed(title=f'봇이 음성채널에 연결되어 있지 않습니다.', color=0xf8e71c)) # 출력
        else:
            await ctx.send(embed=discord.Embed(title=f'당신은 음성채널에 연결되어 있지 않습니다.', description='음성채널에 참여한 유저만 `!음소거`를 사용할 수 있습니다.', color=0xf8e71c)) # 출력



def setup(client):
    client.add_cog(voice(client))