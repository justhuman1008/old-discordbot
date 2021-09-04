import discord
import asyncio
import os
from discord.ext import commands
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re # Regex for youtube link
import warnings
import requests

opggsummonersearch = 'https://www.op.gg/summoner/userName='

tierScore = {
        'default': 0,
        'iron': 1,
        'bronze': 2,
        'silver': 3,
        'gold': 4,
        'platinum': 5,
        'diamond': 6,
        'master': 7,
        'grandmaster': 8,
        'challenger': 9
    }

def deleteTags(htmls):
    for a in range(len(htmls)):
        htmls[a] = re.sub('<.+?>', '', str(htmls[a]), 0).strip()
    return htmls

def tierCompare(solorank, flexrank):
    if tierScore[solorank] > tierScore[flexrank]:
        return 0
    elif tierScore[solorank] < tierScore[flexrank]:
        return 1
    else:
        return 2

warnings.filterwarnings(action='ignore')


class game(commands.Cog): #2
    def __init__(self, bot): #3
        self.bot = bot #4


    @commands.command(aliases=['롤전적', '롤티어'],usage="!롤전적 `{닉네임}`") # Com1
    async def _lol(self, ctx, *, playerNickname):
        playerNickname = playerNickname.replace(" ", "+")
        """롤전적을 보여줍니다."""
        checkURLBool = urlopen(opggsummonersearch + quote(playerNickname))
        bs = BeautifulSoup(checkURLBool, 'html.parser')

        # 자유랭크 언랭은 뒤에 '?image=q_auto&v=1'표현이없다
        RankMedal = bs.findAll('img', {
            'src': re.compile('\/\/[a-z]*\-[A-Za-z]*\.[A-Za-z]*\.[A-Za-z]*\/[A-Za-z]*\/[A-Za-z]*\/[a-z0-9_]*\.png')})
        # index 0 : Solo Rank
        # index 1 : Flexible 5v5 rank

        # for mostUsedChampion
        mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
        mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})

        # 솔랭, 자랭 둘다 배치가 안되어있는경우 -> 사용된 챔피언 자체가 없다. 즉 모스트 챔피언 메뉴를 넣을 필요가 없다.

        if len(playerNickname) == 1:
            embed = discord.Embed(title="소환사 이름이 입력되지 않았습니다!", description="", color=0xffdc16)
            embed.add_field(name="Summoner name not entered",value="To use command !롤전적 : !롤전적 (Summoner Nickname)", inline=False)
            await ctx.send(embed=embed)

        elif len(deleteTags(bs.findAll('h2', {'class': 'Title'}))) != 0:
            embed = discord.Embed(title="존재하지 않는 소환사", description="", color=0xffdc16)
            embed.add_field(name="해당 닉네임의 소환사가 존재하지 않습니다.", value="소환사 이름을 확인해주세요", inline=False)
            await ctx.send(embed=embed)
        else:
            try:
                # Scrape Summoner's Rank information
                # [Solorank,Solorank Tier]
                solorank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {'class': {'RankType', 'TierRank'}}))
                # [Solorank LeaguePoint, Solorank W, Solorank L, Solorank Winratio]
                solorank_Point_and_winratio = deleteTags(
                    bs.findAll('span', {'class': {'LeaguePoints', 'wins', 'losses', 'winratio'}}))
                # [Flex 5:5 Rank,Flexrank Tier,Flextier leaguepoint + W/L,Flextier win ratio]
                flexrank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {
                    'class': {'sub-tier__rank-type', 'sub-tier__rank-tier', 'sub-tier__league-point',
                              'sub-tier__gray-text'}}))
                # ['Flextier W/L]
                flexrank_Point_and_winratio = deleteTags(bs.findAll('span', {'class': {'sub-tier__gray-text'}}))

                # embed.set_imag()는 하나만 들어갈수 있다.

                # 솔랭, 자랭 둘다 배치 안되어있는 경우 -> 모스트 챔피언 출력 X
                if len(solorank_Point_and_winratio) == 0 and len(flexrank_Point_and_winratio) == 0:
                    embed = discord.Embed(title=playerNickname+"님의 전적검색", description=f'[op.gg 바로가기]({opggsummonersearch}{playerNickname})', color=0xffdc16)
                    embed.add_field(name="솔로 : Unranked", value="해당 랭크전을 플레이하지 않음", inline=False)
                    embed.add_field(name="자유 5:5 : Unranked", value="해당 랭크전을 플레이하지 않음", inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    await ctx.send(embed=embed)
                    

                # 솔로랭크 기록이 없는경우
                elif len(solorank_Point_and_winratio) == 0:

                    # most Used Champion Information : Champion Name, KDA, Win Rate
                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    FlexRankTier = '자유 5:5' + ' : ' + flexrank_Types_and_Tier_Info[1]
                    FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + flexrank_Types_and_Tier_Info[-1]
                    
                    embed = discord.Embed(title=playerNickname+"님의 전적검색", description=f'[op.gg 바로가기]({opggsummonersearch}{playerNickname})', color=0xffdc16)
                    embed.add_field(name="솔로 : Unranked", value="해당 랭크전을 플레이하지 않음", inline=False)
                    embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                    embed.add_field(name="주 챔피언 : " + mostUsedChampion,value="KDA : " + mostUsedChampionKDA + " / " + " 승률 : " + mostUsedChampionWinRate,inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[1]['src'])
                    await ctx.send(embed=embed)

                # 자유랭크 기록이 없는경우
                elif len(flexrank_Point_and_winratio) == 0:

                    # most Used Champion Information : Champion Name, KDA, Win Rate
                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()
                    
                    #솔로랭크 정리
                    solorank_Point_and_winratio = [item.replace("Win Ratio", "승률") for item in solorank_Point_and_winratio]
                    SoloRankTier = '솔로' + ' : ' + solorank_Types_and_Tier_Info[1]
                    SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + " / " + solorank_Point_and_winratio[3]+'(' + solorank_Point_and_winratio[1] + " " + solorank_Point_and_winratio[2] + ')'

                    embed = discord.Embed(title=playerNickname+"님의 전적검색", description=f'[op.gg 바로가기]({opggsummonersearch}{playerNickname})', color=0xffdc16)
                    embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                    embed.add_field(name="자유 5:5 : Unranked", value="해당 랭크전을 플레이하지 않음", inline=False)
                    embed.add_field(name="주 챔피언 : " + mostUsedChampion, value="KDA : " + mostUsedChampionKDA + " / " + "승률 : " + mostUsedChampionWinRate,inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    await ctx.send(embed=embed)


                # 두가지 유형의 랭크 모두 완료된사람
                else:
                    # 더 높은 티어를 thumbnail에 안착
                    solorankmedal = RankMedal[0]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')
                    flexrankmedal = RankMedal[1]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')

                    # 솔로랭크 정리
                    solorank_Point_and_winratio = [item.replace("Win Ratio", "승률") for item in solorank_Point_and_winratio]

                    flexrank_Types_and_Tier_Info = [item.replace("LP", " LP") for item in flexrank_Types_and_Tier_Info]
                    flexrank_Types_and_Tier_Info = [item.replace("Win Rate", "승률") for item in flexrank_Types_and_Tier_Info]

                    # Make State
                    SoloRankTier = '솔로' + ' : ' + solorank_Types_and_Tier_Info[1]
                    SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + " / " + solorank_Point_and_winratio[3]+'('+solorank_Point_and_winratio[1] + " " + solorank_Point_and_winratio[2]+')'
                    FlexRankTier = '자유 5:5' + ' : ' + flexrank_Types_and_Tier_Info[1]
                    FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " / " + flexrank_Types_and_Tier_Info[-1]

                    # most Used Champion Information : Champion Name, KDA, Win Rate
                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    cmpTier = tierCompare(solorankmedal[0], flexrankmedal[0])
                    embed = discord.Embed(title=playerNickname+"님의 전적검색", description=f'[op.gg 바로가기]({opggsummonersearch}{playerNickname})', color=0xffdc16)
                    embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                    embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                    embed.add_field(name="주 챔피언 : " + mostUsedChampion,value="KDA : " + mostUsedChampionKDA + " / " + " 승률 : " + mostUsedChampionWinRate,inline=False)


                    if cmpTier == 0:
                        embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    elif cmpTier == 1:
                        embed.set_thumbnail(url='https:' + RankMedal[1]['src'])
                    else:
                        if solorankmedal[1] > flexrankmedal[1]:
                            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                        elif solorankmedal[1] < flexrankmedal[1]:
                            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                        else:
                            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    await ctx.send(embed=embed)

            except HTTPError as e:
                embed = discord.Embed(title=playerNickname+"님의 전적검색 실패", description="", color=0xffdc16)
                embed.add_field(name="", value="올바르지 않은 소환사 이름입니다.", inline=False)
                await ctx.send(embed=embed)

            except UnicodeEncodeError as e:
                embed = discord.Embed(title=playerNickname+"님의 전적검색 실패", description="", color=0xffdc16)
                embed.add_field(name="???", value="올바르지 않은 소환사 이름입니다.", inline=False)
                await ctx.send(embed=embed)

    @commands.command(aliases=['스팀'],usage="!스팀 `{SteamID(17자리 숫자)} / !스팀 `{사용자 지정 URL}`") # Com2
    async def steam(self, ctx, ID):
        profileURL = "https://steamcommunity.com/id/" + ID #기본적으로 개인 URL을 이용
        if ID.isdigit() == True: # ID가 정수일떄
            if len(ID) == 17: # ID가 17자리 숫자일때(스팀 개인코드는 17자리)
                profileURL = "https://steamcommunity.com/profiles/"+ ID #스팀 코드 URL로 변경

        html = requests.get(profileURL).text
        try:
            username = html.split('"personaname":"')[1].split('"')[0]
            embed = discord.Embed(title=username , url=profileURL, color=0xffdc16)
            try:
                data=html.split("This profile is private.")[1]
            except:
                status = ""
                is_Online = html.split('<div class="profile_in_game_header">')[1].split('</div>')[0]
                if is_Online == "Currently Offline":
                    status = "⚪ 오프라인"
                elif is_Online == "Currently In-Game":
                    status = "▶️ 게임 중"
                    status = status + "(" + html.split('<div class="profile_in_game_name">')[1].split('</div>')[0] + ")"
                elif is_Online == "Currently Online":
                    status = "🟢 온라인"
                else:
                    status = is_Online
                icon_url = html.split('<img src="')[5].split('">')[0]
                embed.add_field(name="상태:", value=status, inline=True)
                embed.set_thumbnail(url=icon_url)
                try:
                    since = html.split('since')[1].split('"')[0]
                    embed.add_field(name="최초가입일:", value=since, inline=True)
                except:
                    dummy = 0
                #embed.set_image(url=icon_url)
                try:
                    level = html.split('<span class="friendPlayerLevelNum">')[1].split('</span>')[0]
                    embed.add_field(name="레벨:", value=level, inline=True)
                    local_data = ""
                    for i in range(3):
                        cache_html1 = html.split('<div class="game_name">')[i+1].split('</div>')[0]
                        game_name =  cache_html1.split('">')[1].split('</a>')[0]
                        game_time = html.split('<div class="game_info_details">')[i+1].split('on record')[0].replace("hrs"," 시간")
                        least_game = html.split('last played on')[i+1].split('</div>')[0]
                        #game_time=""
                        local_data = local_data + "**" + game_name + "**:" + game_time + "플레이(마지막 플레이:" + least_game + ")\n"
                    embed.add_field(name="최근 플레이한 게임:", value=local_data, inline=False)
                except:
                    dummy = 0
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="스팀 프로필 검색 실패",description="이 계정은 비공개 계정입니다.", color=0xffdc16)
                await ctx.send(embed=embed)
        except:
            try:
                answer = html.split('<h3>')[1].split('</h3>')[0]
                if answer == "The specified profile could not be found.":
                    answer = "요청하신 계정을 찾을수 없습니다. \n사용자 지정 URL을 설정하지 않았다면 유저코드를 입력해주세요."
                embed = discord.Embed(title="에러!",description=answer, color=0xffdc16)
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(title="에러!",description="알수없는 오류가 발생하였습니다.", color=0xffdc16)
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(game(bot))  