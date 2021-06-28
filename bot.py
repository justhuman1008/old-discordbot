import discord
from discord.ext import commands
import os

client = discord.Client()


token = "NzgwMzY2MDczNjUxMjY1NTM2.X7uCig.LUqtSkbGvKu6mzMhWf-isOIo4Xc"


@client.event
async def on_ready():

    print("=========================")
    print("아래의 계정으로 로그인 합니다 : ")
    print(client.user.name)
    print("연결 성공")
    game = discord.Game("!도움말")
    print("=========================")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_message(message):
    if message.author.bot:
        return None
    if message.content == "!ttest":
        await message.channel.send("전송 완료")
        print("메시지 전송 테스트 진행됨")

client.run(token)