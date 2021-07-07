import requests #pip
import discord
import asyncio
from discord.ext import commands
import json
import bs4 #파싱용
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

    @commands.command(aliases=['접률']) # 마인리스트 파싱
    async def uuid(self, ctx,*,message):
        url = f"https://minelist.kr/servers/{message}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        connect = soup.find("div", attrs={"class":"col-md-6 col-sm-6"}).get_text().strip()

        embed = discord.Embed(title="서버접속 현황", description="`"+connect+"`", color=0xffdc16)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/777089714137595914/externalFile.png")
        embed.set_footer(text="Information in Minelist")
        await ctx.send(embed=embed)






def setup(client):
    client.add_cog(minecraft(client))