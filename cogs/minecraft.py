import requests #pip
import discord
import asyncio
from discord.ext import commands
import json


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


        uuid = "db14a367-08b1-4432-a6d8-4200b69c9083"
        uuid_dashed = "db14a367-08b1-4432-a6d8-4200b69c9083"
        self.API_KEY = "ef31f74e-3700-4f99-a572-a96341c19c31"





def setup(client):
    client.add_cog(minecraft(client))