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

    @commands.command(aliases=['UUID']) # 마인크래프트 UUID
    async def uuid(self, ctx,*,message):

        try:
            mojangAPI = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{message}").json()
            uuid = mojangAPI["id"]
            name = mojangAPI["name"]

            mojangAPI = discord.Embed(title= f"{name}의 UUID", color=0xffdc16, description=f"{uuid}")
            await ctx.send(embed=mojangAPI) 
        except:
            exceptMojangAPI = discord.Embed(title= "UUID 로드 실패", color=0xffdc16, description="아래의 내용을 확인해주세요")
            exceptMojangAPI.add_field(name="­", value=f"닉네임이 `{message}`가 맞는지 확인해주세요.", inline=False)
            exceptMojangAPI.add_field(name="­", value=f"Mojang API가 작동하고 있는지 확인해주세요.", inline=False)
            await ctx.send(embed=exceptMojangAPI)

    @commands.command()
    async def 접률(self, *, ctx):
        res = requests.get('https://minelist.kr/servers/madesv.kr')
        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        try:
            connect = soup.find("div", attrs={"class":"col-md-6 col-sm-6"}).get_text().strip()
            await ctx.send(connect)
        except:
            await ctx.send("마인리스트 접속에 실패하였습니다")



def setup(client):
    client.add_cog(minecraft(client))