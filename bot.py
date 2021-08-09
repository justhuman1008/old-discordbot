import discord #pip
from discord.ext import commands
from discord.ext import tasks
import os # Cogs 로드용
from datetime import datetime # 시간표시용
from itertools import cycle # 주기 생성
import asyncio
from discord.ext.commands.converter import TextChannelConverter

#https://discord.com/api/oauth2/authorize?client_id=857814380749651998&permissions=8&scope=bot
#token = os.getenv("DISCORD_BOT_TOKEN")

now = datetime.now()

client = commands.Bot(command_prefix = '!')

def is_it_me(ctx): #관리자 계정 확인(나)
    return ctx.author.id == 512166620463104004
    #@commands.check(is_it_me) @client.commands 바로 아래 작성

my_id = 512166620463104004

@client.event # 봇 작동
async def on_ready():
    change_status.start()
    print("=========================")
    print("아래의 계정으로 로그인 : ")
    print(client.user.name)
    print("연결에 성공했습니다.")
    print ("가동된 시간 : %s년 %s월 %s일 %s시 %s분" %(now.year, now.month, now.day, now.hour, now.minute))
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
    if ctx.author.id == my_id:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(embed=discord.Embed(title=f'Cog {extension} Loaded', description='Cogs Loaded : %s월 %s일 %s시 %s분' %(now.month, now.day, now.hour, now.minute), color=0xf8e71c))
        print(f'파일 {extension}이 Load됨 : %s월 %s일 %s시 %s분' %(now.month, now.day, now.hour, now.minute))
    else:
        print(f'{ctx.author}님이 {extension}을(를) Load하려 시도하였습니다. : %s월 %s일 %s시 %s분' %(now.month, now.day, now.hour, now.minute))

@client.command() # Cogs 수동 언로드
async def unload(ctx, extension):
    if ctx.author.id == my_id:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(embed=discord.Embed(title=f'Cog {extension} UnLoaded', description='Cogs UnLoaded : %s월 %s일 %s시 %s분' %(now.month, now.day, now.hour, now.minute), color=0xf8e71c))
        print(f'파일 {extension}이 UnLoad됨 : %s월 %s일 %s시 %s분' %(now.month, now.day, now.hour, now.minute))
    else:
        print(f'{ctx.author}님이 {extension}을(를) Unload하려 시도하였습니다. : %s월 %s일 %s시 %s분' %(now.month, now.day, now.hour, now.minute))

@client.command() # Cogs 수동 리로드
async def reload(ctx, extension):
    if ctx.author.id == my_id:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(embed=discord.Embed(title=f'Cog {extension} ReLoaded', description='Cogs ReLoaded : %s월 %s일 %s시 %s분' %(now.month, now.day, now.hour, now.minute), color=0xf8e71c))
        print(f'파일 {extension}이 ReLoad됨 : %s월 %s일 %s시 %s분' %(now.month, now.day, now.hour, now.minute))
    else:
        print(f'{ctx.author}님이 {extension}을(를) Reload하려 시도하였습니다. : %s월 %s일 %s시 %s분' %(now.month, now.day, now.hour, now.minute))


@client.event
async def on_command_error(ctx, error): # 오류처리
    if isinstance(error, commands.CommandNotFound): #없는 명령어 감지 제거
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(title='명령어를 제대로 입력해주세요', color=0xf8e71c))
    elif isinstance(error, commands.BadArgument):
        await ctx.send(embed=discord.Embed(title='명령어를 제대로 입력해주세요', color=0xf8e71c))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(title='{}님은 권한이 부족합니다.'.format(ctx.message.author), color=0xf8e71c))
    else:
        admin = client.get_user(int(my_id))
        embed = discord.Embed(title="오류!!", description="오류가 발생했습니다.", color=0xFF0000)
        embed.add_field(name="상세", value=f"```{error}```")
        await admin.send(embed=embed)



client.remove_command("help")



@client.command(aliases=['청소', '삭제', '지워'],usage="!청소 {N}") # 채팅청소
@commands.has_permissions(manage_messages=True)
async def _clear(ctx, amount : int):
    await ctx.channel.purge(limit=1)
    await ctx.channel.purge(limit=amount)

@client.event #서버에 초대됨
async def on_guild_join(server):
    print(server,"서버에 초대받았습니다!")
    print ("서버에 참여한 시간 : %s년 %s월 %s일 %s시 %s분" %(now.year, now.month, now.day, now.hour, now.minute))


@client.event # 서버에서 추방됨
async def on_guild_remove(server):
    print(server,"서버에서 추방되었습니다..")
    print ("서버에서 추방된 시간 : %s년 %s월 %s일 %s시 %s분" %(now.year, now.month, now.day, now.hour, now.minute))


@client.command(aliases=['Help', 'HELP', '도움', '도움말'])
async def help(ctx):
    comem = discord.Embed(title="그저 평범한 봇 명령어", description="­봇의 접두사는 `!`입니다.", color=0xffdc16)
    comem.add_field(name=':small_blue_diamond:'+"서버관리", value="`!서버정보` `!추방` `!차단` `!차단해제` `!슬로우모드` `!청소` `!초대링크`\n`!역할생성` `!채널생성` `!음성채널생성` `!카테고리생성`", inline=False)
    comem.add_field(name=':small_blue_diamond:'+"검색", value="`!구글` `!네이버` `!코로나` `!멜론차트` `!날씨` `!한강수온` `!인벤뉴스`\n`!롤전적` `!스팀`", inline=False)
    comem.add_field(name=':small_blue_diamond:'+"마인크래프트", value="`!UUID` `!스킨` `!색코드` `!하이픽셀`", inline=False)
    comem.add_field(name=':small_blue_diamond:'+"놀이", value="`!따라하기` `!소수` `!주사위` `!숫자` `!음성` `!참가` `!나가` `!음소거`", inline=False)
    comem.add_field(name=':small_blue_diamond:'+"봇", value="`!도움말` `!정보` `!ping`", inline=False)
    comem.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/865508255144345610/c9dae6501347cb49.jpg')

    helpem = discord.Embed(title="그저 평범한 봇 도움말", description="­봇의 접두사는 `!`입니다.", color=0xffdc16)
    helpem.add_field(name=':small_blue_diamond:'+"!서버관리", value="디스코드 서버 관리용 명령어", inline=False)
    helpem.add_field(name=':small_blue_diamond:'+"!검색", value="검색 명령어 모음", inline=False)
    helpem.add_field(name=':small_blue_diamond:'+"!마인크래프트", value="마인크래프트 관련 명령어", inline=False)
    helpem.add_field(name=':small_blue_diamond:'+"!놀이", value="놀이용 명령어", inline=False)
    helpem.add_field(name=':small_blue_diamond:'+"!봇", value="봇 관리용 명령어", inline=False)
    helpem.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/865508255144345610/c9dae6501347cb49.jpg')

    helpem.add_field(name="­", value="모든 명령어를 확인하려면 `1분 이내` 🔍 클릭", inline=False)
    msg = await ctx.send(embed = helpem)
    helpem.remove_field(6)
    reaction_list = ['🔍', '❌']
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

@client.command(aliases=['명령어'])
async def alcommand(ctx):
    comem = discord.Embed(title="그저 평범한 봇 명령어", description="­봇의 접두사는 `!`입니다.", color=0xffdc16)
    comem.add_field(name=':small_blue_diamond:'+"서버관리", value="`!서버정보` `!추방` `!차단` `!차단해제` `!슬로우모드` `!청소` `!초대링크`\n`!역할생성` `!채널생성` `!음성채널생성` `!카테고리생성`", inline=False)
    comem.add_field(name=':small_blue_diamond:'+"검색", value="`!구글` `!네이버` `!코로나` `!멜론차트` `!날씨` `!한강수온` `!인벤뉴스`\n`!롤전적` `!스팀`", inline=False)
    comem.add_field(name=':small_blue_diamond:'+"마인크래프트", value="`!UUID` `!스킨` `!색코드` `!하이픽셀`", inline=False)
    comem.add_field(name=':small_blue_diamond:'+"놀이", value="`!따라하기` `!소수` `!주사위` `!숫자` `!음성` `!참가` `!나가` `!음소거`", inline=False)
    comem.add_field(name=':small_blue_diamond:'+"봇", value="`!도움말` `!정보` `!ping`", inline=False)
    comem.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/865508255144345610/c9dae6501347cb49.jpg')

    helpem = discord.Embed(title="그저 평범한 봇 도움말", description="­봇의 접두사는 `!`입니다.", color=0xffdc16)
    helpem.add_field(name=':small_blue_diamond:'+"!서버관리", value="디스코드 서버 관리용 명령어", inline=False)
    helpem.add_field(name=':small_blue_diamond:'+"!검색", value="검색 명령어 모음", inline=False)
    helpem.add_field(name=':small_blue_diamond:'+"!마인크래프트", value="마인크래프트 관련 명령어", inline=False)
    helpem.add_field(name=':small_blue_diamond:'+"!놀이", value="놀이용 명령어", inline=False)
    helpem.add_field(name=':small_blue_diamond:'+"!봇", value="봇 관리용 명령어", inline=False)
    helpem.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/865508255144345610/c9dae6501347cb49.jpg')

    comem.add_field(name="­", value="도움말을 확인하려면 `1분 이내` 📎 클릭", inline=False)
    msg = await ctx.send(embed = comem)
    comem.remove_field(6)
    reaction_list = ['📎', '❌']
    for r in reaction_list:
        await msg.add_reaction(r)
    def check(reaction, user):
        return str(reaction) in reaction_list and user == ctx.author and reaction.message.id == msg.id
    try:
        reaction, _user = await client.wait_for("reaction_add", check=check, timeout=60.0)
    except asyncio.TimeoutError:
        await msg.clear_reactions()
    else:
        if str(reaction) == '📎':
            await msg.clear_reactions()
            await msg.edit(embed=helpem)
        if str(reaction) == '❌':
            await msg.clear_reactions()
        pass

client.run('--') 