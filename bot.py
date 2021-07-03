import discord
from discord.ext import commands
import os

client = discord.Client()


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
    if message.content.startswith("!아"): 
        await message.channel.send("아")


client.run(token)