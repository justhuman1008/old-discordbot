import discord #pip
from discord.ext import commands
import asyncio

import setting
Bot_name = setting.Bot_Name
Bot_invite = setting.Bot_invite
Bot_Image = setting.Bot_Image

class bot_utills(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['초대'])
    async def _botinv(self, ctx):
        embed = discord.Embed(title=Bot_name+" 초대하기", description="", color=0xffdc16)
        embed.add_field(name="­", value=f'[{Bot_name} 서버에 추가하기]({Bot_invite})', inline=True)
        embed.set_thumbnail(url=setting.Bot_Image)
        await ctx.send(embed = embed)

    @commands.command(aliases=['봇','정보'])
    async def _botinfo(self, ctx):
        embed = discord.Embed(title=Bot_name, description="­", color=0xffdc16)
        embed.add_field(name="핑", value=f'`{round(self.client.latency * 1000)}ms`', inline=True)
        embed.add_field(name='봇 접두사', value='`!{명령어}`', inline=True)
        embed.add_field(name="­", value="­", inline=True)
        embed.add_field(name="연결된 서버 수", value=f'`{len(self.client.guilds)}개 서버`', inline=True)
        embed.add_field(name="이용중인 유저 수", value=f'`{len(self.client.users)}명`', inline=True)
        embed.add_field(name="­", value="­", inline=True)
        embed.add_field(name="개발 언어", value="`Python`", inline=True)
        embed.add_field(name='GitHub', value='[Bot GitHub](https://github.com/justhuman1008/Just_Bot)', inline=True)
        embed.add_field(name="호스팅", value="[Heroku](https://heroku.com/)", inline=True)
        embed.add_field(name="개발,운영", value="`Just_human1008#8138`", inline=False)
        embed.set_thumbnail(url=Bot_Image)
        await ctx.send(embed=embed)

    @commands.command(aliases=['pong', '핑', '퐁'])
    async def ping(self, ctx):
            async with ctx.typing():
                await asyncio.sleep(0)
                embed = discord.Embed(title = ":ping_pong: 현재 봇의 핑", description = f"{round(self.client.latency * 1000, 3)}ms", colour = discord.Colour(0xffdc16))
                await ctx.send(embed = embed)


    @commands.command(aliases=['테스트', '태스트'])
    async def test(self, ctx):
        await ctx.send('test')

def setup(client):
    client.add_cog(bot_utills(client))