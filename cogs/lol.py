import discord #pip
from discord.ext import commands, tasks
import asyncio
import requests
from urllib.request import urlretrieve
import json
import time
from bs4 import BeautifulSoup


class lol(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['티어'])
    async def tear(self, ctx,*,message):


        Name = message

        try:
            req = requests.get('http://www.op.gg/summoner/userName='+Name)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')

            Champ = [0,1,2,3,4]
            Champ_game = [0,1,2,3,4]
            Champ_ratio = [0,1,2,3,4]


            SoloRank = soup.find_all('div', {'class': 'TierRank'})
            SoloRank2 = str(SoloRank[0])[str(SoloRank[0]).find('TierRank">') + 10:str(SoloRank[0]).find('</div>')]


            Rank_Side = soup.find_all('div', {'class':'SideContent' })

            for side in Rank_Side:
                img = side.find('img')
                img_src = 'https:'+img['src']
            
            if len(SoloRank2) > 35:
                embed_default = discord.Embed(title="롤 전적검색", description="op.gg 를 활용한 전적 검색 봇입니다", color=0xd5d5d5)
                embed_default.add_field(name="닉네임:  "+Name, value="Unranked", inline=False)
                embed_default.set_thumbnail(url=img_src)
                embed_default.set_footer(text='op.gg')
                await ctx.send(embed=embed_default)

            else:

                # 2가 붙은 변수는 print 를 위한 str
                # Embed 구성을 위한 내용 추출
                SoloRank_LP = soup.find_all('span', {'class' : 'LeaguePoints'})
                SoloRank_LP2 = str(SoloRank_LP[0])[str(SoloRank_LP[0]).find('">') + 3:str(SoloRank_LP[0]).find('</span>')]
                SoloRank_wins = soup.find_all('span', {'class': 'wins'})
                SoloRank_wins2 = str(SoloRank_wins[0])[str(SoloRank_wins[0]).find('">') + 2:str(SoloRank_wins[0]).find('</span>')]
                SoloRank_losses = soup.find_all('span', {'class': 'losses'})
                SoloRank_losses2 = str(SoloRank_losses[0])[str(SoloRank_losses[0]).find('">') + 2:str(SoloRank_losses[0]).find('</span>')]
                SoloRank_winratio = soup.find_all('span', {'class': 'winratio'})
                SoloRank_winratio2 = str(SoloRank_winratio[0])[str(SoloRank_winratio[0]).find('">') + 5:str(SoloRank_winratio[0]).find('</span>')]

                # 주목할만한 챔피언 system
                for a in range(0,5):
                    Champion = soup.select('div.ChampionName')[a].text
                    Champ[a] = Champion.strip()
                    Champion_game = soup.select('div.Title')[a].text
                    Champ_game[a] = Champion_game.replace(" Played", "")
                    Champion_ratio = soup.select('div.WinRatio')[a].text
                    Champ_ratio[a] = Champion_ratio.strip()

                # 변수
                ChampList = []  # 20판 이상의 챔피언 등록
                Champ_ratio_Top = 0
                Champ_game_Top = 0
                Champ_index = 0

                for a in range(0,5):
                    if int(Champ_game[a]) > 20:
                        ChampList.append(a)
                    
                    if Champ[a] in ChampList: # 승률 높은 걸로 산출, 승률 같다면 판수 높은 걸로 산출
                        if Champ_ratio_Top == 0 or Champ_ratio[a] > Champ_ratio_Top:
                            Champ_ratio_Top = Champ_ratio[a]
                            Champ_game_Top = Champ_game[a]
                            Champ_index = a
                        elif Champ_ratio[a] == Champ_ratio_Top:
                            if Champ_game[a] > Champ_game_Top:
                                Champ_ratio_Top = Champ_ratio[a]
                                Champ_game_Top = Champ_game[a]
                                Champ_index = a
                            else:
                                continue

                        else:
                            continue
                    else:
                        continue
            
                # Embed 메시지 구성

                # 소환사 아이콘
                Player_image = soup.find_all('img',{'class' : 'ProfileImage'})
                Player_image = str(Player_image[0])[str(Player_image[0]).find('src="') + 5:str(Player_image[0]).find('"/>')]
                Player_image = str("https:"+ Player_image)


                embed = discord.Embed(title="", description="", color=0xd5d5d5)
                embed.set_author(name=Name +"님의 전적 검색", url="http://www.op.gg/summoner/userName="+Name, icon_url=Player_image)
                embed.add_field(name=SoloRank2+SoloRank_LP2, value= SoloRank_wins2 + "  " +SoloRank_losses2 + " | " +SoloRank_winratio2 , inline=True)
                embed.add_field(name="주목할 만한 챔피언", value= Champ[Champ_index] +" "+ Champ_game[Champ_index] +"게임  "+ Champ_ratio[Champ_index], inline= False)
                embed.set_thumbnail(url=img_src)
                embed.set_footer(text='op.gg')


                # 메시지 보내기
                await ctx.send(embed=embed)

        except:
            await ctx.send('닉네임 똑바로')


def setup(client):
    client.add_cog(lol(client))