import discord #pip
from discord.ext import commands, tasks
import random

class ran_game(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['놀이', '게임'])
    async def _rangame(self, ctx):
        embed = discord.Embed(title="놀이 명령어", description="­봇의 접두사는 `!`입니다.", color=0xffdc16)
        embed.add_field(name=':small_blue_diamond:'+"!주사위", value="정육면체 주사위를 굴립니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!숫자", value="1~100중 숫자 하나를 뽑습니다.", inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/780341733128011816/lego.png')
        await ctx.send(embed = embed)


    @commands.command()
    async def 주사위(self, ctx):

        randomNum = random.randrange(1,7)
        if randomNum == 1:
            embed = discord.Embed(title="주사위를 던졌다", description=':game_die: '+ ':one:', color=0xffdc16)
            await ctx.send(embed=embed)
        if randomNum == 2:
            embed = discord.Embed(title="주사위를 던졌다", description=':game_die: '+ ':two:', color=0xffdc16)
            await ctx.send(embed=embed)
        if randomNum == 3:
            embed = discord.Embed(title="주사위를 던졌다", description=':game_die: '+ ':three:', color=0xffdc16)
            await ctx.send(embed=embed)
        if randomNum == 4:
            embed = discord.Embed(title="주사위를 던졌다", description=':game_die: '+ ':four:', color=0xffdc16)
            await ctx.send(embed=embed)
        if randomNum == 5:
            embed = discord.Embed(title="주사위를 던졌다", description=':game_die: '+ ':five:', color=0xffdc16)
            await ctx.send(embed=embed)
        if randomNum == 6:
            embed = discord.Embed(title="주사위를 던졌다", description=':game_die: '+ ':six:', color=0xffdc16)
            await ctx.send(embed=embed)


    @commands.command()
    async def 숫자(self, ctx):
        card = random.randint(1,100)
        embed = discord.Embed(title="랜덤숫자 뽑기", description="­", color=0xffdc16)
        embed.add_field(name=card, value="과연 뭐가 뽑혔을까..", inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/780346351917465600/pcc.png")
        await ctx.send(embed=embed)





def setup(client):
    client.add_cog(ran_game(client))