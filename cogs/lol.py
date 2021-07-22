import requests
import discord
from discord.ext import commands
import asyncio
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import json
import time

class lol(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def 전적(self, ctx):
        embed = discord.Embed(title="전적 검색 도움말", description="­봇의 접두사는 `!`입니다.", color=0xffdc16)
        embed.add_field(name=':small_blue_diamond:'+"!롤티어 `롤 닉네임`", value="롤 티어를 검색합니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"준비중", value=".", inline=False)
        await ctx.send(embed = embed)


    @commands.command(aliases=['롤티어'])
    async def _tear(self, ctx,*,Name):    

            Final_Name = Name.replace(" ","+")
            api_key = "RGAPI-2c129c98-02a7-4217-86fe-f4eeda4df004"
            URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+Final_Name #0.8초 소요
            res = requests.get(URL, headers={"X-Riot-Token": api_key})

            if res.status_code == 200:
                #코드가 200일때
                resobj = json.loads(res.text)
                URL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+resobj["id"]
                player_icon = str(resobj["profileIconId"])
                player_id = str(resobj["id"])
                res = requests.get(URL, headers={"X-Riot-Token": api_key})
                rankinfo = json.loads(res.text) #list class


                if len(rankinfo) == 0:
                    await ctx.send(embed=discord.Embed(title="소환사의 랭크 정보가 없습니다", description="­", color=0xf8e71c))

                for i in rankinfo:
                    if i["queueType"] == "RANKED_SOLO_5x5":
                        rank = str(i["rank"])
                        tier = str(i["tier"])
                        leaguepoints = str(i["leaguePoints"])
                        wins = str(i["wins"])
                        losses = str(i["losses"])
                        ratio = str(round(int(wins)*100/(int(wins)+int(losses)), 1))

                        URL = "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"+player_id
                        res = requests.get(URL, headers={"X-Riot-Token": api_key})
                        player_mastery = json.loads(res.text) # player mastery : list class
                        
                    
                        embed = discord.Embed(title="", description="", color=0xf8e71c)
                        embed.set_author(name=Final_Name  +"님의 전적 검색", url="http://www.op.gg/summoner/userName="+Final_Name, icon_url="http://ddragon.leagueoflegends.com/cdn/10.25.1/img/profileicon/"+player_icon+".png")
                        embed.add_field(name=tier+" "+rank+"   | "+leaguepoints+" LP", value="­", inline=False)
                        embed.add_field(name="승률 : "+ratio+"%",value=wins+"승"+" "+losses +"패", inline= False)
                        embed.set_thumbnail(url="http://z.fow.kr/img/emblem/"+tier.lower()+".png")
                        await ctx.send(embed=embed)
                        break
            else:
                await ctx.send(embed=discord.Embed(title="소환사가 존재하지 않습니다", description="­", color=0xf8e71c))


def setup(client):
    client.add_cog(lol(client))