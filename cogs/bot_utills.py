import discord #pip
from discord.ext import commands
import asyncio

def is_it_me(ctx): #관리자 계정 확인(나)
    return ctx.author.id == 512166620463104004

class bot_utills(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands

    @commands.command(aliases=['봇'])
    async def _bothelp(self, ctx):
        embed = discord.Embed(title="봇 관련 명령어", description="­", color=0xffdc16)
        embed.add_field(name=':small_blue_diamond:'+"!정보", value="봇의 정보를 출력합니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!ping", value="봇의 핑을 출력합니다.", inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/865508255144345610/c9dae6501347cb49.jpg')
        await ctx.send(embed = embed)

    @commands.command()
    async def test(self, ctx):
        await ctx.send('test')


    @commands.command(aliases=['pong', '핑', '퐁'])
    async def ping(self, ctx):
            async with ctx.typing():
                await asyncio.sleep(0)
                embed = discord.Embed(title = ":ping_pong: 현재 봇의 핑", description = f"{round(self.client.latency * 1000, 3)}ms", colour = discord.Colour(0xffdc16))
                await ctx.send(embed = embed)

    @commands.command(name="반응체크")
    async def get_reaction_and_react(self, ctx):
        msg = await ctx.send("1, 2, 3 반응 중 2 반응을 달아주세요.")
        reaction_list = ['1️⃣', '2️⃣', '3️⃣']
        for r in reaction_list:
            await msg.add_reaction(r)
        def check(reaction, user):
            return str(reaction) in reaction_list and user == ctx.author and reaction.message.id == msg.id
        try:
            reaction, _user = await self.client.wait_for("reaction_add", check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send("시간 초과되었습니다.")
        else:
            if str(reaction) == '2️⃣':
                await ctx.send("성공!")
            else:
                await ctx.send("실패!")

            pass

    @commands.command(aliases=['정보'])
    async def _botinfo(self, ctx):
        embed = discord.Embed(title="그저 평범한 봇", description="­", color=0xffdc16)
        embed.add_field(name="핑", value=f'`{round(self.client.latency * 1000)}ms`', inline=True)
        embed.add_field(name='봇 접두사', value='`!{명령어}`', inline=True)
        embed.add_field(name="­", value="­", inline=True)
        embed.add_field(name="연결된 서버 수", value=f'`{len(self.client.guilds)}개 서버`', inline=True)
        embed.add_field(name="이용중인 유저 수", value=f'`{len(self.client.users)}명`', inline=True)
        embed.add_field(name="­", value="­", inline=True)
        embed.add_field(name="개발 언어", value="`Python`", inline=True)
        embed.add_field(name='GitHub', value='[Bot GitHub](https://github.com/justhuman1008/Just_Bot)', inline=True)
        embed.add_field(name="호스팅", value="[Heroku](https://heroku.com/)", inline=True)
        embed.add_field(name="개발,운영", value="`그저 평범한 인간#8138`", inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/865508255144345610/c9dae6501347cb49.jpg')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(bot_utills(client))