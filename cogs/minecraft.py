import requests #pip
import discord
import asyncio
from discord.ext import commands
import json
import bs4 #파싱용
import aiohttp
from bs4 import BeautifulSoup #pip install bs4 #실검파싱

class minecraft(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['마크', '마인크래프트'])
    async def _minecrafthelp(self, ctx):
        embed = discord.Embed(title="마인크래프트 관련 명령어", description="­", color=0xffdc16)
        embed.add_field(name=':small_blue_diamond:'+"!UUID `닉네임`", value="유저의 마인크래프트 UUID를 불러옵니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!스킨 `닉네임`", value="유저의 스킨을 불러옵니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!색코드", value="마인크래프트에서 사용하는 색코드를 보여줍니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!하이픽셀", value="`준비중`", inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/786832203404935168/de2b606ddf81e1e1.png')
        await ctx.send(embed = embed)

    @commands.command(aliases=['UUID'],usage="!UUID `{닉네임}`") # 마인크래프트 UUID
    async def uuid(self, ctx,*,message):

        try:
            mojangAPI = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{message}").json()
            uuid = mojangAPI["id"]
            name = mojangAPI["name"]

            mojangAPI = discord.Embed(title= f"{name}의 UUID", color=0xffdc16, description=f"{uuid}")
            mojangAPI.set_thumbnail(url=f"https://crafatar.com/avatars/{uuid}.png?overlay")
            await ctx.send(embed=mojangAPI) 
        except:
            exceptMojangAPI = discord.Embed(title= "UUID 로드 실패", color=0xffdc16, description="아래의 내용을 확인해주세요")
            exceptMojangAPI.add_field(name="­", value=f"닉네임이 `{message}`이(가) 맞는지 확인해주세요.", inline=False)
            exceptMojangAPI.add_field(name="­", value=f"[Mojang API](https://api.mojang.com/users/profiles/minecraft/{message})가 작동하고 있는지 확인해주세요.", inline=False)
            await ctx.send(embed=exceptMojangAPI)

    @commands.command(aliases=['SKIN', '스킨'],usage="!스킨 `{닉네임}`") # 마인크래프트 UUID
    async def skin(self, ctx,*,message):
        try:
            mojangAPI = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{message}").json()
            uuid = mojangAPI["id"]
            name = mojangAPI["name"]

            embed = discord.Embed(title=f"{name}님의 스킨", description=f"[스킨 다운로드](https://minecraftskinstealer.com/api/v1/skin/download/skin/{message})", color=0xffdc16)
            try:
                SkinAPI = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{message}").json()
            except:
                embed = discord.Embed(title= "스킨 로드 실패", color=0xffdc16, description="아래의 내용을 확인해주세요")
                embed.add_field(name="­", value=f"닉네임이 `{message}`이(가) 맞는지 확인해주세요.", inline=False)
                embed.add_field(name="­", value=f"[Mojang API](https://api.mojang.com/users/profiles/minecraft/{message})가 작동하고 있는지 확인해주세요.", inline=False)
                embed.add_field(name="­", value=f"[스킨 사이트](https://api.mojang.com/users/profiles/minecraft/{message})가 작동하고 있는지 확인해주세요.", inline=False)
                await ctx.send(embed=embed)

            embed.set_image(url=f"https://crafatar.com/renders/body/{uuid}.png?overlay")
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title= "스킨 로드 실패", color=0xffdc16, description="아래의 내용을 확인해주세요")
            embed.add_field(name="­", value=f"닉네임이 `{message}`이(가) 맞는지 확인해주세요.", inline=False)
            embed.add_field(name="­", value=f"[Mojang API](https://api.mojang.com/users/profiles/minecraft/{message})가 작동하고 있는지 확인해주세요.", inline=False)
            await ctx.send(embed=embed)

    @commands.command(aliases=['색코드']) # 마인크래프트 UUID
    async def micol(self, ctx):
        embed = discord.Embed(title="마인크래프트 색코드", color=0xffdc16)
        embed.set_image(url="https://cdn.discordapp.com/attachments/731471072310067221/869864828053880892/9455efa95e1734a9.png")
        await ctx.send(embed=embed)

#    @commands.command(aliases=['마인리스트']) # 마인리스트 파싱
#    async def minelist(self, ctx,* ,message):
#        url = f"https://minelist.kr/servers/{message}"
#        res = requests.get(url)
#        soup = BeautifulSoup(res.text, "html.parser")
#
#        server = soup.find("i", attrs={"class":"glyphicon glyphicon-ok"}).get_text().strip()
#        embed1 = discord.Embed(title="서버이름", description=f"`{server}`", color=0xffdc16)
#        embed1.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/777089714137595914/externalFile.png")
#        embed1.set_footer(text="Information in Minelist")
#
#        await ctx.send(embed=embed1)







def setup(client):
    client.add_cog(minecraft(client))