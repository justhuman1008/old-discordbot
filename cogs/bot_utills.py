import discord #pip
from discord.ext import commands


class bot_utills(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands

    @commands.command()
    async def test(self, ctx):
        await ctx.send('test')

    @commands.command()
    async def 도움(self, ctx):
        embed = discord.Embed(title="그저 평범한 봇 Help", description="­", color=0xffdc16)
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
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/780365519705473035/externalFile.png")
        await ctx.send(embed=embed)

    @commands.command(aliases=['pong', '핑', '퐁'])
    async def ping(self, ctx):
        embed = discord.Embed(title = ":ping_pong: 현재 봇의 핑", description = f"약{round(self.client.latency * 1000, 3)}ms", colour = discord.Colour(0xffdc16))
        await ctx.send(embed = embed)

    @commands.command(aliases=['정보'])
    async def botinfo(self, ctx):
        embed = discord.Embed(title="그저 평범한 봇 Info", description="­", color=0xffdc16)
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
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(bot_utills(client))