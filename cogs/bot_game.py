import discord #pip
from discord.ext import commands, tasks
import random
import math
import asyncio
from datetime import datetime # 시간표시용

now = datetime.now()

class bot_game(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['놀이', '게임'])
    async def _gamehelp(self, ctx):
        embed = discord.Embed(title="놀이 명령어", description="­", color=0xffdc16)
        embed.add_field(name=':small_blue_diamond:'+"!따라하기 `{채팅}`", value="{채팅}을 따라합니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!소수 `{N}`", value="{N}이 소수인지 확인합니다.", inline=False)
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

    @commands.command(aliases=['따라하기', '따라해'],usage="!따라하기 `{말}`")
    async def _repeat(self, ctx, *, content):
        if "@everyone" in content or "@here" in content:
            embed = discord.Embed(title="`@everyone`이나 `@here`이 포함된 채팅은 따라하지 않습니다.",color=0xffdc16)
            await ctx.channel.send(embed=embed)
        else:
            msg = await ctx.send(f"{content}")
            await msg.add_reaction("💬")



            

    @commands.command(aliases=['소수'],usage="!소수 `{N}`")
    async def _isprime(self, ctx, num: int):
        isprime = discord.Embed(title=f"{num}은 소수입니다.", description=f'[{num}이 왜 소수인가요?](https://www.integers.co/questions-answers/is-{num}-a-prime-number.html)', color=0xffdc16)
        isprime.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/777101285525684234/mathmu.png")

        noprime = discord.Embed(title=f"{num}은 소수가 아닙니다.", description=f'[{num}이 왜 소수가 아닌가요?](https://www.integers.co/questions-answers/is-{num}-a-prime-number.html)', color=0xffdc16)
        noprime.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/777101285525684234/mathmu.png")

        if num == 0: # 0은 자동으로 소수아님 출력
            prime0 = discord.Embed(title=f'0은 소수가 아닙니다.', description=f"[소수 - 지식백과](https://terms.naver.com/entry.naver?docId=1113970&cid=40942&categoryId=32206)", color=0xf8e71c)
            prime0.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/777101285525684234/mathmu.png")
            return await ctx.send(embed=prime0)
        elif num < 0: # 음수는 자동으로 소수아님 출력
            primeu0 = discord.Embed(title=f'음수({num})는 소수가 아닙니다.', description=f"[소수 - 지식백과](https://terms.naver.com/entry.naver?docId=1113970&cid=40942&categoryId=32206)", color=0xf8e71c)
            primeu0.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/777101285525684234/mathmu.png")
            return await ctx.send(embed=primeu0)
        elif num == 1: # 1은 자동으로 소수아님 출력
            return await ctx.send(embed=noprime)
        elif num in [2, 3, 5, 7]: # 2,3,5,7은 자동으로 소수임 출력
            return await ctx.send(embed=isprime)
        elif num % 2 == 0: # 2의 약수는 자동으로 소수아님 출력
            return await ctx.send(embed=noprime)
        elif num % 5 == 0: # 5의 약수는 자동으로 소수아님 출력
            return await ctx.send(embed=isprime)
        elif num >= 1000000001:  # 소수 확인 제한(현재 10억)
            await ctx.send(embed=discord.Embed(title=f'10억 이상의 수는 확인할 수 없습니다.', description=f'확인을 시도한 수 {num}', color=0xf8e71c))
            return
        a = 3
        while a <= math.sqrt(num):
            if num % a == 0:
                return await ctx.send(embed=noprime)#Composite. {0} mod {1} = 0.'.format(num, a)
            a = a + (2, 4)[a % 10 == 3]  # Skips 5s and even numbers
        return await ctx.send(embed=isprime)

def setup(client):
    client.add_cog(bot_game(client))