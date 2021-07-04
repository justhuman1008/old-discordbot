import discord #pip
from discord.ext import commands, tasks
import os # Cogs 로드용
from datetime import datetime # 시간표시용
from itertools import cycle # 주기 생성

#https://discord.com/api/oauth2/authorize?client_id=857814380749651998&permissions=8&scope=bot
#token = os.getenv("DISCORD_BOT_TOKEN")

now = datetime.now()

client = commands.Bot(command_prefix = '!')

@client.event # 봇 작동
async def on_ready():
    change_status.start()
    print("=========================")
    print("아래의 계정으로 로그인 : ")
    print(client.user.name)
    print("연결에 성공했습니다.")
    print ("가동된 시간 : %s년 %s월 %s일 %s시 %s분" %(now.year, now.month, now.day, now.hour, now.minute))
    print("=========================")

Status = cycle(['!help', 'Minecraft', '!help', '!help'])
@tasks.loop(seconds=10) # 상태메시지 변경
async def change_status():
    await client.change_presence(activity=discord.Game(next(Status)))

def is_it_me(ctx): 
    return ctx.author.id == 512166620463104004

@client.command() # Cogs 수동 로드
@commands.check(is_it_me)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(embed=discord.Embed(title=f'Cog {extension} Loaded', description='Cogs Loaded : %s월 %s일 %s시 %s분' %(now.month, now.day, now.hour, now.minute), color=0x909fd4))
    print(f'파일 {extension}이 Load됨 : %s월 %s일 %s시 %s분' %(now.month, now.day, now.hour, now.minute))

@client.command() # Cogs 수동 언로드
@commands.check(is_it_me)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(embed=discord.Embed(title=f'Cog {extension} UnLoaded', description='Cogs UnLoaded : %s월 %s일 %s시 %s분' %(now.month, now.day, now.hour, now.minute), color=0x909fd4))
    print(f'파일 {extension}이 UnLoad됨 : %s월 %s일 %s시 %s분' %(now.month, now.day, now.hour, now.minute))

@client.command() # Cogs 수동 리로드
@commands.check(is_it_me)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(embed=discord.Embed(title=f'Cog {extension} ReLoaded', description='Cogs ReLoaded : %s월 %s일 %s시 %s분' %(now.month, now.day, now.hour, now.minute), color=0x909fd4))
    print(f'파일 {extension}이 ReLoad됨 : %s월 %s일 %s시 %s분' %(now.month, now.day, now.hour, now.minute))

for filename in os.listdir('./cogs'): # Cogs 자동 로드(봇 작동시)
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'{filename[:-3]}가 정상적으로 로드되었습니다.')

@client.command() # 채팅청소
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('삭제할 수를 입력해주세요')



@client.event # 서버에서 초대됨
async def on_guild_join(server):
    print(server,"서버에 초대받았습니다!")
    print ("서버에 참여한 시간 : %s년 %s월 %s일 %s시 %s분" %(now.year, now.month, now.day, now.hour, now.minute))

@client.event # 서버에서 추방됨
async def on_guild_remove(server):
    print(server,"서버에서 추방되었습니다..")
    print ("서버에서 추방된 시간 : %s년 %s월 %s일 %s시 %s분" %(now.year, now.month, now.day, now.hour, now.minute))

client.run('token') 