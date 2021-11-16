import discord
from discord.ext import commands
from discord.utils import get
import asyncio
from bs4 import BeautifulSoup
import requests
import urllib
import urllib.parse
from urllib import parse
import xml.etree.ElementTree as ET
from urllib.request import urlopen, Request
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.parse import quote
from requests import get, post
import aiohttp 
import json




class search(commands.Cog): 

    def __init__(self, bot): 
        self.bot = bot 


    @commands.command(aliases=['구글'],usage="!구글 `{내용}`") # Com2
    async def _google(self, ctx, search):
        url = 'https://www.google.com/search?q='+search

        embed = discord.Embed(title="구글 검색", description=f"[{search} - Google 검색]({url})", color=0xffdc16)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/782799810905767966/google-logos-2018-5.png')
        await ctx.send(embed=embed)

    @commands.command(aliases=['네이버'],usage="!네이버 `{내용}`") # Com3
    async def _naver(self, ctx, search):
        url = 'https://search.naver.com/search.naver?query='+search

        embed = discord.Embed(title="네이버 검색", description=f"[{search} : 네이버 통합 검색]({url})", color=0xffdc16)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/777091660865339402/nalogo.png')
        await ctx.send(embed=embed)

    @commands.command(aliases=['인벤뉴스']) # Com4
    async def _inven(self, ctx):
        embed = discord.Embed(title="인벤 주요뉴스",description="[인벤 뉴스 바로가기](http://www.inven.co.kr/webzine/news/?hotnews=1)", color=0xffdc16)
        targetSite = 'http://www.inven.co.kr/webzine/news/?hotnews=1'
        print(f'인벤 주요뉴스를 출력하기 위해 인벤에 접속을 시도합니다.')
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
        print(f'인벤 주요뉴스 출력 완료')


    @commands.command(aliases=['멜론차트','노래순위']) # Com5
    async def _melon(self, ctx):
        print(f'멜론차트를 출력하기 위해 멜론에 접속을 시도합니다.')
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
        print(f'멜론차트 출력 완료')

    @commands.command(aliases=['날씨'],usage="!날씨 `{지역명}`") # Com6
    async def weather(self, ctx, location):
        print(f'날씨를 출력하기 위해 네이버에 접속을 시도합니다.')
        try:
            # 네이버 연결
            enc_location = urllib.parse.quote(location+'날씨')
            hdr = {'User-Agent': 'Mozilla/5.0'}
            url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + enc_location
            req = Request(url, headers=hdr)
            html = urllib.request.urlopen(req)
            bsObj = BeautifulSoup(html, "html.parser")
            print(' -네이버 접속에 성공하였습니다.')

            area = bsObj.find('h2', {'class': 'title'}) # 지역명
            area = area.text
            print(f' -지역명 로드에 성공했습니다. [{area}]')

            Temp = bsObj.find('div', {'class': 'temperature_text'}).get_text() # 현재 온도
            find_num = Temp.find('도')+1
            Temp = Temp[find_num:]
            print(f' -현재 온도 로드에 성공하였습니다. [{Temp}]')

            MXLW_Temp = bsObj.find('div', {'class': 'cell_temperature'}).get_text() # 오늘 최저/최고 온도
            MXLW_Temp = MXLW_Temp.replace("기온","기온: ")
            print(f' -최저/최고 기온 로드에 성공하였습니다.[{MXLW_Temp}]')

            Cast = bsObj.find('p', {'class': 'summary'}).get_text() # 기상정보 요약
            Cast = Cast.replace("기온","기온: ")
            Cast = Cast.replace("요","요 / ")
            if Cast.find('높아요') > -1:
                Cast = Cast.replace('높아요', '낮아요')
            elif Cast.find('낮아요') > -1:
                rainper = Cast.replace('낮아요', '높아요')
            print(f' -기상정보 요약 로드에 성공하였습니다.[{Cast}]')

            rainper = bsObj.select('dd', {'class': 'desc'})[0].get_text() # 강수확률
            print(f' -강수확률 로드에 성공하였습니다.[{rainper}]')

            vapor = bsObj.select('dd', {'class': 'desc'})[1].get_text() # 습도
            print(f' -습도 로드에 성공하였습니다.[{vapor}]')

            wind = bsObj.select('dd', {'class': 'desc'})[2].get_text() # 바람
            print(f' -바람 로드에 성공하였습니다.[{wind}]')


            weather = discord.Embed(title=area+ ' 날씨 정보', description=f'[네이버 날씨 바로가기]({url})', color=0xffdc16)
            weather.add_field(name="현재 상태",value=Cast)
            weather.add_field(name='현재 온도', value=Temp+'C', inline=False)
            weather.add_field(name='오늘 최저/최고 기온', value=MXLW_Temp, inline=False)
            weather.add_field(name='현재 강수확률', value=rainper, inline=False)
            weather.add_field(name='현재 습도', value=vapor, inline=False)
            weather.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/867995043473018950/pngwing.com.png')
            print(' -네이버로부터 받은 날씨를 임베드에 입력하였습니다.')

            try:
                Sunbox = bsObj.find('li', {'class': 'item_today level3'}) # 자외선지수
                Sunlight = Sunbox.text
                Sunlight = Sunlight.replace("  자외선 ","")
                print(f' -자외선 지수 로드에 성공하였습니다.[{Sunlight}]')
                weather.add_field(name='현재 자외선 수치', value=Sunlight, inline=False)
            except:
                Sunlight = "Not Detected"

            Sunset = bsObj.find('li', {'class': 'item_today type_sun'}).get_text() # 자외선지수
            print(f' -일몰시간 로드에 성공하였습니다.[{Sunset}]')

            if Cast.find("맑음") > -1:
                weather.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/882529428054368316/01.png')
                print(' -날씨 인식후 이미지를 변경하였습니다.(맑음)')
            elif Cast.find("흐림") > -1:
                weather.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/881831929127776327/07.png')
                print(' -날씨 인식후 이미지를 변경하였습니다.(흐림)')
            elif Cast.find("구름많음") > -1:
                weather.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/881831910626717696/05.png')
                print(' -날씨 인식후 이미지를 변경하였습니다.(구름많음)')
            elif Cast.find("비") > -1:
                weather.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/881832630876778526/09.png')
                print(' -날씨 인식후 이미지를 변경하였습니다.(비)')
            else:
                print('입력되지 않은 날씨추이로 인해 기본 날씨 이미지를 전송하였습니다.')


            await ctx.send(embed=weather)
            print(f'날씨 출력 완료')
        except:
            print(f'`{location}`의 날씨 출력에 실패하였습니다.')
            embed = discord.Embed(title= "날씨 불러오기 실패", color=0xffdc16, description="아래의 내용을 확인해주세요")
            embed.add_field(name=f"지역명이 `{location}`이(가) 맞는지 확인해주세요.", value=f"지역단위가 작다면(ex (읍,면,동)) `속한 지자체를 같이 입력`해보세요", inline=False)
            embed.add_field(name="­네이버 검색이 작동하고 있는지 확인해주세요.", value="­", inline=False)
            await ctx.send(embed=embed)

    @commands.command(aliases=['한강','한강수온']) # Com7
    async def 수온(self, ctx):
        print(f'한강수온을 검색하기 위해 사이트에 접속을 시도합니다.')
        req = Request("http://hangang.dkserver.wo.tc/")
        webpage = urlopen(req).read()
        output = json.loads(webpage)
        temp = output['temp']
        time = output['time']
        embed = discord.Embed(title=f"현재 한강 수온은 {temp}°C", description=f"들어가기 딱 좋은 온도", color=0xffdc16)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/867993227742035988/gksrks.jpg')
        await ctx.send(embed=embed)
        print(f'한강수온 출력 완료')

    @commands.command(name="코로나",ailases=["코로나바이러스", "우한폐렴", "신종코로나", "신종코로나바이러스", "코로나19"]) # Com8
    async def ncov2019(self, ctx):
        print(f'코로나 현황을 검색하기 위해 사이트에 접속을 시도합니다.')
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(
                "http://ncov.mohw.go.kr/index_main.jsp"
            ) as r:
                soup = BeautifulSoup(await r.text(), "html.parser")
                boardList = soup.select("ul.liveNum > li > span")
                newstNews = soup.select(".m_news > ul > li > a")[0]


        boardList = [x.text for x in boardList]
        boardList = [item.replace("(누적)", "") for item in boardList]
        boardList = [item.replace("전일대비", "") for item in boardList]

        embed = discord.Embed(title="코로나-19 국내 현황",description="[예방수칙](http://www.cdc.go.kr/gallery.es?mid=a20503020000&bid=0003)",color=0xD8EF56)
        embed.add_field(name="확진", value="\n".join(boardList[0:2]))
        embed.add_field(name="완치", value=" ".join(boardList[2:4]))
        embed.add_field(name="사망", value=" ".join(boardList[6:8]), inline=True)
        embed.add_field(name="코로나-19 최신 브리핑",value="[{}](http://ncov.mohw.go.kr{})".format(newstNews.text, newstNews.get("href")),inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/869449509359484991/af275a5f9980be9e.png')
        await ctx.send(embed=embed)
        print(f'코로나-19 국내 현황 출력 완료')



def setup(bot):
    bot.add_cog(search(bot))