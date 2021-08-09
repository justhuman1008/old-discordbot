import requests #pip
import discord
import asyncio
from discord.ext import commands
import json
import bs4 #파싱용
import aiohttp
from bs4 import BeautifulSoup #pip install bs4 #실검파싱
from datetime import datetime # 시간표시용

now = datetime.now()

def findUUID(nickname):        
    try:
        print("------------------------------")
        print(f'{nickname}의 UUID를 찾기 위해 모장 API에 접속을 시도합니다.')
        mojangAPI = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{nickname}").json()
        uuid = mojangAPI["id"]
        name = mojangAPI["name"]
        print(f'{name}의 UUID: {uuid}')
        print(f'{nickname}의 닉네임과 UUID를 확인하였습니다.')
        print("------------------------------")
        return name, uuid
    except :
        uuid = 'Not Found'
        name = 'Not Found'
        print(f'{nickname}의 UUID를 찾을 수 없습니다.')
        print("------------------------------")
        return name, uuid

class minecraft(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['마크', '마인크래프트'])
    async def _minecrafthelp(self, ctx):
        embed = discord.Embed(title="마인크래프트 관련 명령어", description="­", color=0xffdc16)
        embed.add_field(name=':small_blue_diamond:'+"!마크구매", value="마인크래프트 Java Edition 구매 링크를 출력합니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!UUID `닉네임`", value="유저의 마인크래프트 UUID를 불러옵니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!스킨 `닉네임`", value="유저의 스킨을 불러옵니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!색코드", value="마인크래프트에서 사용하는 색코드를 보여줍니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!하이픽셀", value="`준비중`", inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/786832203404935168/de2b606ddf81e1e1.png')
        await ctx.send(embed = embed)



    @commands.command(aliases=['UUID'],usage="!UUID `{닉네임}`")
    async def uuid(self, ctx,*,message):
        name, uuid = findUUID(message)
        if name == 'Not Found':
            NfoundUUID = discord.Embed(title= "UUID 로드 실패", color=0xffdc16, description="아래의 내용을 확인해주세요")
            NfoundUUID.add_field(name="­", value=f"닉네임이 `{message}`이(가) 맞는지 확인해주세요.", inline=False)
            NfoundUUID.add_field(name="­", value=f"[Mojang API](https://api.mojang.com/users/profiles/minecraft/{message})가 작동하고 있는지 확인해주세요.", inline=False)
            await ctx.send(embed=NfoundUUID)
        else:
            foundUUID = discord.Embed(title= f"{name}의 UUID", color=0xffdc16, description=f"{uuid}")
            foundUUID.set_thumbnail(url=f"https://crafatar.com/avatars/{uuid}.png?overlay")
            await ctx.send(embed=foundUUID)


    @commands.command(aliases=['SKIN', '스킨'],usage="!스킨 `{닉네임}`")
    async def skin(self, ctx,*,message):
        name, uuid = findUUID(message)
        if name == 'Not Found':
            NfoundUUID = discord.Embed(title= "스킨 로드 실패", color=0xffdc16, description="아래의 내용을 확인해주세요")
            NfoundUUID.add_field(name="­", value=f"닉네임이 `{message}`이(가) 맞는지 확인해주세요.", inline=False)
            NfoundUUID.add_field(name="­", value=f"[Mojang API](https://api.mojang.com/users/profiles/minecraft/{message})가 작동하고 있는지 확인해주세요.", inline=False)
            await ctx.send(embed=NfoundUUID)
        else:
            foundSKIN = discord.Embed(title=f"{name}님의 스킨", description=f"[스킨 다운로드](https://minecraftskinstealer.com/api/v1/skin/download/skin/{message})", color=0xffdc16)
            foundSKIN.set_image(url=f"https://crafatar.com/renders/body/{uuid}.png?overlay")
            await ctx.send(embed=foundSKIN)

    @commands.command(aliases=['마크구매', '마인크래프트구매'])
    async def _bymic(self, ctx):
        buyminecraft = discord.Embed(title="Minecraft Java Edition", description="[MINECRAFT 구매](https://www.minecraft.net/ko-kr/store/minecraft-java-edition)", color=0xffdc16)
        buyminecraft.add_field(name="판매가: ₩30,000",value="한국에 있는 플레이어의 경우 \nMinecraft를 이용하려면 만19세 이상이어야 합니다.",inline=False)
        buyminecraft.add_field(name="­", value="▫️ Windows, Linux 및 Mac에서 이용 가능\n▫️ 사용자 제작 스킨 및 모드 지원\n▫️ Java 에디션용 렐름과 호환\n▫️ 새로운 기능을 일찍 접해볼 수 있는 스냅샷 액세스\n▫️ 게임 런처를 통해 수시로 업데이트\n▫️ 무료 체험판 버전 이용가능\n\n시스템 요구 사항을 확인하려면 🖥️ 클릭", inline=False)
        buyminecraft.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/874171555003912192/9aa60a6fb4157e44.jpg")

        minecraftcom = discord.Embed(title="Minecraft: Java Edition 시스템 요구 사항", description="최소 사양", color=0xffdc16)
        minecraftcom.add_field(name="CPU",value="Intel Core i3-3210 / AMD A8-7600과 동급 장치",inline=False)
        minecraftcom.add_field(name="GPU",value="내장: Intel HD Graphics 4000(Ivy Bridge) / AMD Radeon R5 시리즈\n외장: Nvidia GeForce 400 시리즈 / AMD Radeon HD 7000 시리즈",inline=False)
        minecraftcom.add_field(name="RAM",value="4GB",inline=False)
        minecraftcom.add_field(name="HDD",value="게임 코어, 지도 및 기타 파일을 위해 최소 1GB",inline=False)
        minecraftcom.add_field(name="OS",value="Windows: Windows 7 이상\nmacOS: Any 64-bit OS X using 10.9 Maverick or newer\nLinux: Any modern 64-bit distributions from 2014 onwards\n\nMinecraft 파일 최초 다운로드하려면 인터넷 연결이 필요하며, \n다운로드 이후 오프라인으로 플레이가 가능합니다.",inline=False)
        minecraftcom.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/874171555003912192/9aa60a6fb4157e44.jpg")

        msg = await ctx.send(embed = buyminecraft)
        reaction_list = ['🖥️']
        for r in reaction_list:
            await msg.add_reaction(r)
        def check(reaction, user):
            return str(reaction) in reaction_list and user == ctx.author and reaction.message.id == msg.id
        try:
            reaction, _user = await self.client.wait_for("reaction_add", check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await msg.clear_reactions()
        else:
            if str(reaction) == '🖥️':
                await msg.clear_reactions()
                await msg.edit(embed=minecraftcom)
            if str(reaction) == '❌':
                await msg.clear_reactions()
            pass

    @commands.command(aliases=['색코드'])
    async def _micol(self, ctx):
        embed = discord.Embed(title="마인크래프트 색코드", color=0xffdc16)
        embed.set_image(url="https://cdn.discordapp.com/attachments/731471072310067221/869864828053880892/9455efa95e1734a9.png")
        await ctx.send(embed=embed)








def setup(client):
    client.add_cog(minecraft(client))