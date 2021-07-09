import discord
from bs4 import BeautifulSoup
import requests

token = "tke"


url = "https://minelist.kr/servers/madesv.kr"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")



@discord.client.event
async def on_message(message):
    if message.content.startswith("서버정보"):
        connect = soup.find("div", attrs={"class":"col-md-12 server-info top container-fluid"}).get_text().strip()
        embed = discord.Embed(title="서버정보", description="", color=0x62c1cc)
        embed.add_field(name="서버정보", value=connect, inline=False)
        await message.channel.send(embed=embed)


discord.client.run(token)