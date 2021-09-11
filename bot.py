import discord #pip
from discord.ext import commands
from discord.ext import tasks
import os # Cogs 로드용
from datetime import datetime # 시간표시용
import pytz # 시간대 변경
from itertools import cycle # 주기 생성
import asyncio
from discord.ext.commands.converter import TextChannelConverter
import time
import sys

import setting
Owner_ID = setting.Bot_Owner
now_kst = setting.Now_KST
Bot_name = setting.Bot_Name
Bot_Image = setting.Bot_Image
Owner_Name = setting.Owner_Name
Bot_TOKEN = setting.Bot_TOKEN

if Bot_TOKEN == "봇 토큰":
    print("=========================")
    print("에러!!")
    print('토큰을 `setting.py`에 입력해주세요')
    print("=========================")
    sys.exit()

client = commands.Bot(command_prefix = setting.Bot_Prefix)


@client.event # 봇 작동
async def on_ready():
    change_status.start()
    print("=========================")
    print("아래의 계정으로 로그인 : ")
    print(client.user.name)
    print("연결에 성공했습니다.")
    print ("가동된 시간 : "+now_kst)
    print("=========================")


for filename in os.listdir('./cogs'): # Cogs 자동 로드(봇 작동시)
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'{filename[:-3]}가 정상적으로 로드되었습니다.')

Status = cycle(['!help', 'Minecraft', '!help', '!help'])
@tasks.loop(seconds=10) # 상태메시지 자동 변경
async def change_status():
    await client.change_presence(activity=discord.Game(next(Status)))


@client.command() # Cogs 수동 로드
async def load(ctx, extension):
    if str(ctx.author.id) == Owner_ID:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(embed=discord.Embed(title=f'Cog {extension} Loaded', description='Cogs Loaded : '+now_kst, color=0xf8e71c))
        print(f'파일 {extension}이 Load됨 : '+now_kst)
    else:
        print(f'{ctx.author}님이 {extension}을(를) Load하려 시도하였습니다. : '+now_kst)

@client.command() # Cogs 수동 언로드
async def unload(ctx, extension):
    if str(ctx.author.id) == Owner_ID:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(embed=discord.Embed(title=f'Cog {extension} UnLoaded', description='Cogs UnLoaded : '+now_kst, color=0xf8e71c))
        print(f'파일 {extension}이 UnLoad됨 : '+now_kst)
    else:
        print(f'{ctx.author}님이 {extension}을(를) Unload하려 시도하였습니다. : '+now_kst)

@client.command() # Cogs 수동 리로드
async def reload(ctx, extension):
    if str(ctx.author.id) == Owner_ID:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(embed=discord.Embed(title=f'Cog {extension} ReLoaded', description='Cogs ReLoaded : '+now_kst, color=0xf8e71c))
        print(f'파일 {extension}이 ReLoad됨 : '+now_kst)
    else:
        print(f'{ctx.author}님이 {extension}을(를) Reload하려 시도하였습니다. : '+now_kst)


@client.event
async def on_command_error(ctx, error): # 오류처리
    if isinstance(error, commands.CommandNotFound): #없는 명령어 감지 제거
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(title='{필수값}을 입력해주세요', color=0xf8e71c))
    elif isinstance(error, commands.BadArgument):
        await ctx.send(embed=discord.Embed(title='{필수값}을 제대로 입력해주세요', color=0xf8e71c))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(title='{}님은 권한이 부족합니다.'.format(ctx.message.author), color=0xf8e71c))
    else:
        print("=========================")
        print('* 오류 발생 '+now_kst)
        print(f"{error}")
        print("=========================")

@client.event #서버에 초대됨
async def on_guild_join(server):
    print(server,"서버에 초대받았습니다!")
    print ("서버에 참여한 시간 : "+now_kst)

@client.event # 서버에서 추방됨
async def on_guild_remove(server):
    print(server,"서버에서 추방되었습니다..")
    print ("서버에서 추방된 시간 : "+now_kst)


client.remove_command("help")

@client.command(aliases=['청소', '삭제', '지워'],usage="!청소 {N}")
@commands.has_permissions(manage_messages=True)
async def _clear(ctx, amount : int):
    await ctx.channel.purge(limit=1)
    await ctx.channel.purge(limit=amount)

@client.command(aliases=['hellothisisverification'],usage="개발자확인용")#한국봇리스트 인증용
async def _checkbotowner(ctx):
    await ctx.send(Owner_Name)

@client.command(aliases=['Help', 'HELP', '도움', '도움말'])
async def help(ctx,commands="No Category"):

    #도움말
    helpem = discord.Embed(title=Bot_name+" 도움말", description="­봇의 접두사는 `!`입니다.", color=0xffdc16)
    helpem.add_field(name=':small_blue_diamond:'+"!도움말 서버관리", value="디스코드 서버 관리용 명령어", inline=False)
    helpem.add_field(name=':small_blue_diamond:'+"!도움말 검색", value="검색 명령어 모음", inline=False)
    helpem.add_field(name=':small_blue_diamond:'+"!도움말 마인크래프트", value="마인크래프트 관련 명령어", inline=False)
    helpem.add_field(name=':small_blue_diamond:'+"!도움말 놀이", value="놀이용 명령어", inline=False)
    helpem.add_field(name=':small_blue_diamond:'+"!도움말 음성", value="디스코드 통화방 관련 명령어", inline=False)
    helpem.add_field(name=':small_blue_diamond:'+"!도움말 자가진단", value="교육청 자가진단 관련 명령어", inline=False)
    helpem.add_field(name=':small_blue_diamond:'+"!도움말 봇", value="봇 관리용 명령어", inline=False)
    helpem.add_field(name="­", value='🔍 `!명령어` 입력시 모든 명령어 확인 가능', inline=False)
    helpem.set_thumbnail(url=Bot_Image)

    #서버관리
    serverem = discord.Embed(title="서버 관리용 명령어", description="­", color=0xffdc16)
    serverem.add_field(name=':small_blue_diamond:'+"!서버정보", value="서버에 대한 정보를 출력합니다.", inline=False)
    serverem.add_field(name=':small_blue_diamond:'+"!추방 `{멘션}`", value="멘션한 유저를 추방합니다.", inline=False)
    serverem.add_field(name=':small_blue_diamond:'+"!차단 `{멘션}`", value="`멘션한 유저를 차단합니다.", inline=False)
    serverem.add_field(name=':small_blue_diamond:'+"!차단해제 `닉네임#태그`", value="해당 유저를 차단해제합니다.", inline=False)
    serverem.add_field(name=':small_blue_diamond:'+"!슬로우모드 `{N}`", value="{N}초 만큼 슬로우모드를 적용합니다.", inline=False)
    serverem.add_field(name=':small_blue_diamond:'+"!청소 `{N}`", value="{N}만큼 메시지를 삭제합니다.", inline=False)
    serverem.add_field(name=':small_blue_diamond:'+"!초대링크 `[N]`", value="서버 초대링크([N]회 제한)를 생성합니다.", inline=False)
    serverem.add_field(name=':small_blue_diamond:'+"!역할생성 `{역할명}`", value="{역할명} 역할을 생성합니다.", inline=False)
    serverem.add_field(name=':small_blue_diamond:'+"!채널생성 `{채널명}`", value="{채널명} 채널을 생성합니다.", inline=False)
    serverem.add_field(name=':small_blue_diamond:'+"!음성채널생성 `{채널명}`", value="{채널명} 채널을 생성합니다.", inline=False)
    serverem.add_field(name=':small_blue_diamond:'+"!카테고리생성 `{카테고리명}`", value="{카테고리명} 카테고리를 생성합니다.", inline=False)
    serverem.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/777102022771343370/cust.png')

    #검색
    searchem = discord.Embed(title="사이트 검색 명령어", description="­", color=0xffdc16)
    searchem.add_field(name=':small_blue_diamond:'+"!구글 `{내용}`", value="{내용}을 구글에서 검색합니다.", inline=False)
    searchem.add_field(name=':small_blue_diamond:'+"!네이버 `{내용}`", value="{내용}을 네이버에서 검색합니다.", inline=False)
    searchem.add_field(name=':small_blue_diamond:'+"!롤전적 `{닉네임}`", value="{닉네임}의 롤 전적을 불러옵니다.", inline=False)
    searchem.add_field(name=':small_blue_diamond:'+"!스팀 `{SteamID(17자리 숫자)} or {사용자 지정 URL}`", value="{-}의 스팀 프로필을 불러옵니다.", inline=False)
    searchem.add_field(name=':small_blue_diamond:'+"!코로나", value="국내 코로나-19 현황을 불러옵니다.", inline=False)
    searchem.add_field(name=':small_blue_diamond:'+"!멜론차트", value="멜론차트를 불러옵니다.", inline=False)
    searchem.add_field(name=':small_blue_diamond:'+"!날씨 `{지역}`", value="{지역}의 날씨를 검색합니다.\n타지역 날씨가 뜰 시 지역이 속한 지자체도 같이 입력해주세요.", inline=False)
    searchem.add_field(name=':small_blue_diamond:'+"!한강수온", value="현재 한강의 수온을 불러옵니다.", inline=False)
    searchem.add_field(name=':small_blue_diamond:'+"!인벤뉴스", value="인벤의 주요뉴스를 불러옵니다.", inline=False)
    searchem.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/867992533509210152/pngegg.png')

    #마인크래프트
    mincrfem = discord.Embed(title="마인크래프트 관련 명령어", description="­", color=0xffdc16)
    mincrfem.add_field(name=':small_blue_diamond:'+"!UUID `{닉네임}`", value="`{닉네임}`의 마인크래프트 UUID를 불러옵니다.", inline=False)
    mincrfem.add_field(name=':small_blue_diamond:'+"!스킨 `{닉네임}`", value="`{닉네임}`의 스킨을 불러옵니다.", inline=False)
    mincrfem.add_field(name=':small_blue_diamond:'+"!마크 구매", value="마인크래프트 Java Edition 구매 링크를 출력합니다.", inline=False)
    mincrfem.add_field(name=':small_blue_diamond:'+"!마크 사양 `[권장/최소]`", value="마인크래프트 Java Edition `[권장/최소]` 사양을 출력합니다.", inline=False)
    mincrfem.add_field(name=':small_blue_diamond:'+"!마크 날씨", value="마인크래프트 날씨 목록을 출력합니다.", inline=False)
    mincrfem.add_field(name=':small_blue_diamond:'+"!마크 세계", value="마인크래프트 세계 목록을 출력합니다.", inline=False)
    mincrfem.add_field(name=':small_blue_diamond:'+"!발전과제 `[발전과제분류]`", value="마인크래프트 발전과제 목록을 출력합니다.", inline=False)
    mincrfem.add_field(name=':small_blue_diamond:'+"!하이픽셀", value="`준비중`", inline=False)
    mincrfem.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/786832203404935168/de2b606ddf81e1e1.png')

    #놀이
    botplayem = discord.Embed(title="놀이 명령어", description="­", color=0xffdc16)
    botplayem.add_field(name=':small_blue_diamond:'+"!따라하기 `{채팅}`", value="{채팅}을 따라합니다.", inline=False)
    botplayem.add_field(name=':small_blue_diamond:'+"!소수 `{N}`", value="{N}이 소수인지 확인합니다.", inline=False)
    botplayem.add_field(name=':small_blue_diamond:'+"!주사위", value="정육면체 주사위를 굴립니다.", inline=False)
    botplayem.add_field(name=':small_blue_diamond:'+"!숫자", value="1~100중 숫자 하나를 뽑습니다.", inline=False)
    botplayem.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/780341733128011816/lego.png')

    #음성
    voiceem = discord.Embed(title="음성 채널 관련 명령어", description="­", color=0xffdc16)
    voiceem.add_field(name=':small_blue_diamond:'+"!참가", value="유저가 참여중인 음성채널에 연결합니다.", inline=False)
    voiceem.add_field(name=':small_blue_diamond:'+"!나가", value="음성채널에서 나갑니다.", inline=False)
    voiceem.add_field(name=':small_blue_diamond:'+"!음소거", value="봇의 마이크를 끕니다.", inline=False)
    voiceem.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/870547423196499968/3faa9d34cc341657.png')

    #자가진단
    hssckem = discord.Embed(title="자가진단 관련 명령어", description="현재 자가진단 시스템은 IP 차단으로 인해 이용이 불가능합니다.", color=0xffdc16)
    hssckem.add_field(name=':small_blue_diamond:'+"!자가진단 \n      `{본명}` `{진단비번}` `{생년월일}` `{지역}` `{학교급}` `{학교명}`", value="입력된 정보로 교육청 자가진단을 진행합니다.\n(`!진단정보`로 정보를 입력했다면 정보를 입력하지 않아도 작동)", inline=False)
    hssckem.add_field(name=':small_blue_diamond:'+"!일괄진단", value="봇에 등록된 진단정보 전부 자동으로 자가진단을 진행합니다.", inline=False)
    hssckem.add_field(name=':small_blue_diamond:'+"!진단정보등록 \n      `{본명}` `{진단비번}` `{생년월일}` `{지역}` `{학교급}` `{학교명}`", value="봇에 자가진단 정보를 암호화하여 저장합니다.\n(매일 7시~ 7시 20분 사이에 자동으로 자가진단을 진행합니다.)", inline=False)
    hssckem.add_field(name=':small_blue_diamond:'+"!진단정보삭제", value="본인이 입력한 자가진단 정보를 삭제합니다.", inline=False)
    hssckem.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/880753863328690176/ef6ce3bd06622059.png')

    #봇
    botcmdem = discord.Embed(title="봇 관련 명령어", description="­", color=0xffdc16)
    botcmdem.add_field(name=':small_blue_diamond:'+"!정보", value="봇의 정보를 출력합니다.", inline=False)
    botcmdem.add_field(name=':small_blue_diamond:'+"!도움말", value="봇 도움말을 출력합니다.", inline=False)
    botcmdem.add_field(name=':small_blue_diamond:'+"!명령어", value="봇 명령어를 출력합니다.", inline=False)
    botcmdem.add_field(name=':small_blue_diamond:'+"!회원가입", value="회원가입을 진행합니다.", inline=False)
    botcmdem.add_field(name=':small_blue_diamond:'+"!탈퇴", value="회원탈퇴를 진행합니다.", inline=False)
    botcmdem.add_field(name=':small_blue_diamond:'+"!초대", value=Bot_name+"의 초대링크를 출력합니다.", inline=False)
    botcmdem.add_field(name=':small_blue_diamond:'+"!ping", value="봇의 핑을 출력합니다.", inline=False)
    botcmdem.set_thumbnail(url=Bot_Image)

    if commands == "No Category": # 기본 도움말
        await ctx.send(embed=helpem)
        return

    editguild = ["서버","서버관리","처벌"]
    if commands in editguild:
        await ctx.send(embed = serverem)
        return

    if commands == "검색":
        await ctx.send(embed=searchem)
        return

    mincrf = ["마크","마인크래프트","minecraft","MINECRAFT"]
    if commands in mincrf:
        await ctx.send(embed=mincrfem)
        return

    if commands == "놀이":
        await ctx.send(embed=botplayem)
        return

    voice = ["음성","통화","통화방"]
    if commands in voice:
        await ctx.send(embed=voiceem)
        return

    if commands == "자가진단":
        await ctx.send(embed=hssckem)
        return

    if commands == "봇":
        await ctx.send(embed=botcmdem)
        return
        
    else:
        await ctx.send(embed=discord.Embed(title='오류! 존재하지 않는 도움말입니다', color=0xf8e71c))



@client.command(aliases=['명령어'])
async def alcommand(ctx,admin="Just Commands"):
    # 일반 커맨드 목록
    cmdem = discord.Embed(title=Bot_name+" 명령어", description="­봇의 접두사는 `!`입니다.", color=0xffdc16)
    cmdem.add_field(name=':small_blue_diamond:'+"서버관리", value="`!서버정보` `!추방` `!차단` `!차단해제` `!슬로우모드` `!청소` `!초대링크`\n`!역할생성` `!채널생성` `!음성채널생성` `!카테고리생성`", inline=False)
    cmdem.add_field(name=':small_blue_diamond:'+"검색", value="`!구글` `!네이버` `!코로나` `!멜론차트` `!날씨` `!한강수온` `!인벤뉴스`\n`!롤전적` `!스팀`", inline=False)
    cmdem.add_field(name=':small_blue_diamond:'+"마인크래프트", value="`!마크 구매` `!마크 사양` `!마크 날씨` `!마크 세계` `!마크 색코드`\n`!발전과제` `!UUID` `!스킨` `!하이픽셀`", inline=False)
    cmdem.add_field(name=':small_blue_diamond:'+"놀이", value="`!따라하기` `!소수` `!주사위` `!숫자`", inline=False)
    cmdem.add_field(name=':small_blue_diamond:'+"음성", value="`!참가` `!나가` `!음소거`", inline=False)
    cmdem.add_field(name=':small_blue_diamond:'+"자가진단", value="`!자가진단` `!진단정보등록` `!일괄진단`", inline=False)
    cmdem.add_field(name=':small_blue_diamond:'+"봇", value="`!정보` `!도움말` `!명령어` `!회원가입` `!탈퇴` `!초대` `!ping`", inline=False)
    cmdem.set_thumbnail(url=Bot_Image)

    # 관리자 명령어 목록
    admincmd = discord.Embed(title="봇 제어 명령어", description="­", color=0xffdc16)
    admincmd.add_field(name=':small_blue_diamond:'+"!load `{Cog Name}`", value="{Cog}를 로드(가동)합니다.", inline=False)
    admincmd.add_field(name=':small_blue_diamond:'+"!unload `{Cog Name}`", value="{Cog}를 언로드(가동 중지)합니다.", inline=False)
    admincmd.add_field(name=':small_blue_diamond:'+"!reload `{Cog Name}`", value="{Cog}를 리로드(재가동)합니다.", inline=False)
    admincmd.add_field(name=':small_blue_diamond:'+"!DB저장", value="봇 DB를 관리자 메일로 전송합니다.", inline=False)
    admincmd.add_field(name=':small_blue_diamond:'+"!회원초기화", value="봇 회원 DB를 초기화(전부 제거)합니다.", inline=False)
    admincmd.add_field(name=':small_blue_diamond:'+"!진단정보초기화", value="자가진단정보 DB를 초기화(전부 제거)합니다.", inline=False)
    admincmd.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/777102022771343370/cust.png')

    adcmdck = ["봇관리","관리자","제어"]
    if admin == "Just Commands":
        await ctx.send(embed=cmdem)
        return
    if admin in adcmdck:
        if str(ctx.author.id) == Owner_ID:
            await ctx.send(embed=admincmd)
            return
        else:
            print(f'{ctx.author}님이 관리자 명령어를 보려 시도하였습니다. : '+now_kst)
            return


client.run(setting.Bot_TOKEN) 

'''  유저의 반응에 응답하기
        helpem.add_field(name="­", value="모든 명령어를 확인하려면 `1분 이내` 🔍 클릭", inline=False)
        msg = await ctx.send(embed = helpem)
        helpem.remove_field(6)
        reaction_list = ['🔍', '❌']#⬅️
        for r in reaction_list:
            await msg.add_reaction(r)
        def check(reaction, user):
            return str(reaction) in reaction_list and user == ctx.author and reaction.message.id == msg.id
        try:
            reaction, _user = await client.wait_for("reaction_add", check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await msg.clear_reactions()
        else:
            if str(reaction) == '🔍':
                await msg.clear_reactions()
                await msg.edit(embed=comem)
            if str(reaction) == '❌':
                await msg.clear_reactions()
            pass
'''