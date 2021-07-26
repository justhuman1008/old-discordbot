import asyncio
import discord
from discord.ext import commands
import random
from discord.utils import get
import youtube_dl
from bs4 import BeautifulSoup
import urllib
import requests
from urllib.request import urlopen, Request
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.parse import quote
from urllib import parse
import json
import datetime
import aiohttp
from requests import get, post
from os import environ

class search(commands.Cog): 

    def __init__(self, bot): 
        self.bot = bot 

    @commands.command(aliases=['검색', '인터넷'])
    async def _searchhelp(self, ctx):
        embed = discord.Embed(title="사이트 검색 명령어", description="­", color=0xffdc16)
        embed.add_field(name=':small_blue_diamond:'+"!구글 `{내용}`", value="{내용}을 구글에서 검색합니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!네이버 `{내용}`", value="{내용}을 네이버에서 검색합니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!멜론차트", value="멜론차트를 불러옵니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!날씨 `{지역}`", value="{지역}의 날씨를 검색합니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!한강수온", value="현재 한강의 수온을 불러옵니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!인벤뉴스", value="인벤의 주요뉴스를 불러옵니다.", inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/867992533509210152/pngegg.png')
        await ctx.send(embed = embed)

    @commands.command(aliases=['구글'])
    async def _google(self, ctx, search):
        url = 'https://www.google.com/search?q='+search

        embed = discord.Embed(title="구글 검색", description=f"[{search} - Google 검색]({url})", color=0xffdc16)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/782799810905767966/google-logos-2018-5.png')
        await ctx.send(embed=embed)

    @commands.command(aliases=['네이버'])
    async def _naver(self, ctx, search):
        url = 'https://search.naver.com/search.naver?query='+search

        embed = discord.Embed(title="네이버 검색", description=f"[{search} : 네이버 통합 검색]({url})", color=0xffdc16)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/777091660865339402/nalogo.png')
        await ctx.send(embed=embed)

    @commands.command(aliases=['인벤뉴스'])
    async def _inven(self, ctx):
        """인벤의 주요뉴스를 보여줍니다"""
        embed = discord.Embed(title="인벤 주요뉴스",description="[인벤 뉴스 바로가기](http://www.inven.co.kr/webzine/news/?hotnews=1)", color=0xffdc16)
        targetSite = 'http://www.inven.co.kr/webzine/news/?hotnews=1'

        header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        melonrqRetry = requests.get(targetSite, headers=header)
        melonht = melonrqRetry.text
        melonsp = BeautifulSoup(melonht, 'html.parser')
        artists = melonsp.findAll('span', {'class': 'title'})
        titles = melonsp.findAll('span', {'class': 'summary'})
        for i in range(5):
            artist = artists[i].text.strip()
            title = titles[i].text.strip()
            embed.add_field(name="{0:3d}. {1}".format(i + 1, artist), value='{0}'.format(title), inline=False)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/869039284731133972/3b429bed8d202ca5.png')
        await ctx.send(embed=embed)


    @commands.command(aliases=['멜론차트','노래순위'])
    async def _musicadad(self, ctx):
        """멜론차트를 모여줍니다."""
        embed = discord.Embed(
            title="멜론 음악차트", description="[멜론차트 바로가기](https://www.melon.com/chart/index.htm)", color=0xffdc16)
        targetSite = 'https://www.melon.com/chart/index.htm'

        header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        melonrqRetry = requests.get(targetSite, headers=header)
        melonht = melonrqRetry.text
        melonsp = BeautifulSoup(melonht, 'html.parser')
        artists = melonsp.findAll('span', {'class': 'checkEllipsis'})
        titles = melonsp.findAll('div', {'class': 'ellipsis rank01'})
        for i in range(10):
            artist = artists[i].text.strip()
            title = titles[i].text.strip()
            embed.add_field(name="{0:3d}위 : {1}".format(i + 1, title), value='{0} - {1}'.format(artist, title), inline=False)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/867995777719500881/1.png')
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['날씨'])
    async def weather(self, ctx, location):
        enc_location = urllib.parse.quote(location+'날씨')
        hdr = {'User-Agent': 'Mozilla/5.0'}
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + enc_location
        req = Request(url, headers=hdr)
        html = urllib.request.urlopen(req)
        bsObj = BeautifulSoup(html, "html.parser")
        todayBase = bsObj.find('div', {'class': 'main_info'})

        todayTemp1 = todayBase.find('span', {'class': 'todaytemp'})
        todayTemp = todayTemp1.text.strip()  # 온도

        todayValueBase = todayBase.find('ul', {'class': 'info_list'})
        todayValue2 = todayValueBase.find('p', {'class': 'cast_txt'})
        todayValue = todayValue2.text.strip()  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌

        todayFeelingTemp1 = todayValueBase.find('span', {'class': 'sensible'})
        todayFeelingTemp = todayFeelingTemp1.text.strip()  # 체감온도

        todayMiseaMongi1 = bsObj.find('div', {'class': 'sub_info'})
        todayMiseaMongi2 = todayMiseaMongi1.find('div', {'class': 'detail_box'})
        todayMiseaMongi3 = todayMiseaMongi2.find('dd')
        todayMiseaMongi = todayMiseaMongi3.text  # 미세먼지

        tomorrowBase = bsObj.find('div', {'class': 'table_info weekly _weeklyWeather'})
        tomorrowTemp1 = tomorrowBase.find('li', {'class': 'date_info'})
        tomorrowTemp2 = tomorrowTemp1.find('dl')
        tomorrowTemp3 = tomorrowTemp2.find('dd')
        tomorrowTemp = tomorrowTemp3.text.strip()  # 오늘 오전,오후온도


        embed = discord.Embed(title=location+ ' 날씨 정보', description='[네이버 날씨 바로가기](https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query='+enc_location+')', color=0xffdc16)
        embed.add_field(name='현재온도', value=todayTemp+'˚', inline=False)  # 현재온도
        embed.add_field(name='체감온도', value=todayFeelingTemp, inline=False)  # 체감온도
        embed.add_field(name='현재상태', value=todayValue, inline=False)  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
        embed.add_field(name='현재 미세먼지 상태', value=todayMiseaMongi, inline=False)  # 오늘 미세먼지
        embed.add_field(name='오늘 오전/오후 날씨', value=tomorrowTemp, inline=False)  # 오늘날씨 # color=discord.Color.blue()
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/867995043473018950/pngwing.com.png')
        await ctx.send(embed=embed)

    @commands.command(aliases=['한강','한강수온'])
    async def 수온(self, ctx):
        req = Request("http://hangang.dkserver.wo.tc/")
        webpage = urlopen(req).read()
        output = json.loads(webpage)
        temp = output['temp']
        time = output['time']
        embed = discord.Embed(title=f"현재 한강 수온은 {temp}°C", description=f"들어가기 딱 좋은 온도", color=0xffdc16)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/867993227742035988/gksrks.jpg')
#        embed.set_footer(text=f"측정시간 : {time}")
        await ctx.send(embed=embed)
    
    
def setup(bot):
    bot.add_cog(search(bot))