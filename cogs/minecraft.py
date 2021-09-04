import discord
import requests
import asyncio
from discord.ext import commands
import time


def findUUID(nickname):        
    try:
        print("------------------------------")
        print(f'{nickname}의 UUID를 찾기 위해 모장 API에 접속을 시도합니다.')
        mojangAPI = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{nickname}").json()
        uuid = mojangAPI["id"]
        name = mojangAPI["name"]
        print(f'{name}의 UUID: {uuid}')
        print(f'{nickname}의 닉네임과 UUID를 확인하였습니다.')
        print("------------------------------")
        return name, uuid
    except :
        uuid = 'Not Found'
        name = 'Not Found'
        print(f'{nickname}의 UUID를 찾을 수 없습니다.')
        print("------------------------------")
        return name, uuid

class minecraft(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['UUID'],usage="!UUID `{닉네임}`") # Com2
    async def uuid(self, ctx,*,message):
        name, uuid = findUUID(message)
        if name == 'Not Found':
            NfoundUUID = discord.Embed(title= "UUID 로드 실패", color=0xffdc16, description="아래의 내용을 확인해주세요")
            NfoundUUID.add_field(name="­", value=f"닉네임이 `{message}`이(가) 맞는지 확인해주세요.", inline=False)
            NfoundUUID.add_field(name="­", value=f"[Mojang API](https://api.mojang.com/users/profiles/minecraft/{message})가 작동하고 있는지 확인해주세요.", inline=False)
            await ctx.send(embed=NfoundUUID)
        else:
            foundUUID = discord.Embed(title= f"{name}의 UUID", color=0xffdc16, description=f"{uuid}")
            foundUUID.set_thumbnail(url=f"https://crafatar.com/avatars/{uuid}.png?overlay")
            await ctx.send(embed=foundUUID)

    @commands.command(aliases=['SKIN', '스킨'],usage="!스킨 `{닉네임}`") # Com3
    async def skin(self, ctx,*,message):
        name, uuid = findUUID(message)
        if name == 'Not Found':
            NfoundUUID = discord.Embed(title= "스킨 로드 실패", color=0xffdc16, description="아래의 내용을 확인해주세요")
            NfoundUUID.add_field(name="­", value=f"닉네임이 `{message}`이(가) 맞는지 확인해주세요.", inline=False)
            NfoundUUID.add_field(name="­", value=f"[Mojang API](https://api.mojang.com/users/profiles/minecraft/{message})가 작동하고 있는지 확인해주세요.", inline=False)
            await ctx.send(embed=NfoundUUID)
        else:
            foundSKIN = discord.Embed(title=f"{name}님의 스킨", description=f"[스킨 다운로드](https://minecraftskinstealer.com/api/v1/skin/download/skin/{message})", color=0xffdc16)
            foundSKIN.set_image(url=f"https://crafatar.com/renders/body/{uuid}.png?overlay")
            await ctx.send(embed=foundSKIN)

    @commands.command(aliases=['마크', '마인크래프트'])
    async def mincrft(self, ctx, commands="No Category",first="None"):

        if commands == "No Category":
            mincrfte = discord.Embed(title="Minecraft", description="Minecraft는 Mojang Studios의 설립자\n 마르쿠스 페르손(노치)이 만든 샌드박스 건설 게임이며, Infiniminer, 드워프 포트리스, 던전 키퍼 등에서 영감을 받았다.\n\n이 게임은 3차원 세상에서 블록을 배치하고 부수며,\n 여러 구조물과 작품을 보는 등 수많은 행동을 가능하게 해준다.\n[Minecraft 한국어 위키](https://minecraft.fandom.com/ko/wiki/Minecraft_Wiki)", color=0xffdc16)
            mincrfte.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/882143990525329438/Mclogo.png")
            await ctx.send(embed=mincrfte)

        if commands == "구매":
            buymincrf = discord.Embed(title="Minecraft Java Edition", description="[MINECRAFT 구매](https://www.minecraft.net/ko-kr/store/minecraft-java-edition)", color=0xffdc16)
            buymincrf.add_field(name="판매가: ₩30,000",value="한국에 있는 플레이어의 경우 \nMinecraft를 이용하려면 만19세 이상이어야 합니다.",inline=False)
            buymincrf.add_field(name="­", value="▫️ Windows, Linux 및 Mac에서 이용 가능\n▫️ 사용자 제작 스킨 및 모드 지원\n▫️ Java 에디션용 렐름과 호환\n▫️ 새로운 기능을 일찍 접해볼 수 있는 스냅샷 액세스\n▫️ 게임 런처를 통해 수시로 업데이트\n▫️ 무료 체험판 버전 이용가능", inline=False)
            buymincrf.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/874171555003912192/9aa60a6fb4157e44.jpg")
            await ctx.send(embed=buymincrf)

        if commands == "날씨":
            weather = discord.Embed(title="Minecraft 날씨", description="", color=0xffdc16)
            weather.add_field(name="맑음(clear)",value="공허, 네더, 엔드의 날씨(고정)",inline=False)
            weather.add_field(name="비(rain)",value="◦ 블록이나 몹에 붙은 불이 꺼진다.\n◦ 말라 있는 경작지가 젖어든다.\n◦ 가마솥에 약 5%의 확률로 한 칸 차오른다.\n◦ 낚싯대의 찌가 더 자주 흔들린다.\n◦ 급류가 부여된 삼지창을 육지에서도 사용 할 수 있다.",inline=False)
            weather.add_field(name="눈(Snowfall)",value="기온이 0.15 이하인 지대에서 비(rain)을 대체하는 날씨\n◦ 블럭 위에 약 5%의 확률로 눈이 한 층 쌓인다.",inline=False)
            weather.add_field(name="비와 천둥(Thunderstorm)",value="기온이 0.15 이하인 지대에서는 비 대신 눈이 내린다.\n◦ 삼지창에 인챈트된 집전을 활용 할 수 있다.\n◦ 매초마다 0.02%의 확률로 벼락(Lightning)이 발생한다.",inline=False)
            await ctx.send(embed=weather)

        if commands == "세계":
            mincrfW = discord.Embed(title="Minecraft 세계", description="", color=0xffdc16)
            mincrfW.add_field(name="기본(Normal)",value="◦ 마인크래프트의 기본적인 세계.",inline=False)
            mincrfW.add_field(name="완전한 평지(Superflat)",value="◦ 완전히 평평한 세계.",inline=False)
            mincrfW.add_field(name="넓은 생물군계(Large Biomes)",value="◦ 한 생물군계당 차지하는 면적이 매우 넓은 세계.",inline=False)
            mincrfW.add_field(name="증폭(AMPLIFIED)",value="◦ 매우 높고 험난한 지형으로 이루어진 세계.",inline=False)
            mincrfW.add_field(name="단일 생물군계(Single Biome)",value="◦ 하나의 생물군계로만 이루어진 세계.",inline=False)
            mincrfW.add_field(name="동굴(Caves)",value="◦ 네더와 비슷한 구조로 어두컴컴한 동굴로 이루어진 세계.",inline=False)
            mincrfW.add_field(name="공중 섬(Floating Island)",value="◦ 엔드와 비슷한 구조로 공중에 뜬 땅덩이 조각들로 이루어진 세계",inline=False)
            mincrfW.add_field(name="디버그 모드(Debug Mode)",value="Alt키를 누른 채로 '세계 유형' 버튼 7번 클릭시 선택이 가능하다.\n◦ 모든 블록(모드 포함)들이 일정한 간격을 두고 나란히 설치되어 있다.",inline=False)
            await ctx.send(embed=mincrfW)

        if commands == "색코드":
            mincrfcol = discord.Embed(title="마인크래프트 색코드", color=0xffdc16)
            mincrfcol.set_image(url="https://cdn.discordapp.com/attachments/731471072310067221/869864828053880892/9455efa95e1734a9.png")
            await ctx.send(embed=mincrfcol)

        if commands == "사양":
            cp1mincrf = discord.Embed(title="Minecraft: Java Edition 시스템 요구 사항", description="최소 사양", color=0xffdc16)
            cp1mincrf.add_field(name="CPU",value="Intel Core i3-3210 / AMD A8-7600과 동급 장치",inline=False)
            cp1mincrf.add_field(name="GPU",value="내장: Intel HD Graphics 4000(Ivy Bridge) / AMD Radeon R5 시리즈\n외장: Nvidia GeForce 400 시리즈 / AMD Radeon HD 7000 시리즈",inline=False)
            cp1mincrf.add_field(name="RAM",value="4GB",inline=False)
            cp1mincrf.add_field(name="HDD",value="게임 코어, 지도 및 기타 파일을 위해 최소 1GB",inline=False)
            cp1mincrf.add_field(name="OS",value="Windows: Windows 7 이상\nmacOS: Any 64-bit OS X using 10.9 Maverick or newer\nLinux: Any modern 64-bit distributions from 2014 onwards\n\nMinecraft 파일 최초 다운로드시 인터넷 연결이 필요하며, \n다운로드 이후 오프라인으로 플레이가 가능합니다.",inline=False)
            cp1mincrf.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/874171555003912192/9aa60a6fb4157e44.jpg")

            cp2mincrf = discord.Embed(title="Minecraft: Java Edition 시스템 요구 사항", description="권장 사양", color=0xffdc16)
            cp2mincrf.add_field(name="CPU",value="Intel Core i5-4690 / AMD A10-7800 APU 또는 동급 장치",inline=False)
            cp2mincrf.add_field(name="GPU",value="외장: GeForce 700 시리즈 / AMD Radeon Rx 200 시리즈",inline=False)
            cp2mincrf.add_field(name="RAM",value="8GB",inline=False)
            cp2mincrf.add_field(name="HDD",value="4GB(SSD 권장)",inline=False)
            cp2mincrf.add_field(name="OS",value="Windows: Windows 10\nmacOS: macOS 10.12 Sierra\nLinux: Any modern distributions from 2014 onwards\n\nMinecraft 파일 최초 다운로드시 인터넷 연결이 필요하며, \n다운로드 이후 오프라인으로 플레이가 가능합니다.",inline=False)
            cp2mincrf.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/874171555003912192/9aa60a6fb4157e44.jpg")

            if first == "최소":
                await ctx.send(embed=cp1mincrf)
                return
            if first == "권장":
                await ctx.send(embed=cp2mincrf)
                return
            if first == "None":
                await ctx.send(embed=cp2mincrf)
                return
            else:
                await ctx.send(embed=cp2mincrf)
                return


    @commands.command(aliases=['발전과제','도전과제'],usage="!발전과제 `{발전과제구분}`")
    async def _advce(self, ctx, List="No Category"):

        AdvCategory = discord.Embed(title="Minecraft 발전과제", description="­", color=0xffdc16)
        AdvCategory.add_field(name="Minecraft",value="조합대 획득시 시작",inline=False)
        AdvCategory.add_field(name="네더(Nether)",value="네더 진입시 시작",inline=False)
        AdvCategory.add_field(name="엔드(The End)",value="엔드 진입시 시작",inline=False)
        AdvCategory.add_field(name="모험(Adventure)",value="사망하거나 엔티티를 죽이면 시작",inline=False)
        AdvCategory.add_field(name="농사(Husbandry)",value="음식 섭취시 해금",inline=False)

        mincrft_page1 = discord.Embed(title="Minecraft", description="­", color=0xffdc16)
        mincrft_page1.add_field(name="Minecraft",value="게임의 핵심과 이야기",inline=False)
        mincrft_page1.add_field(name="석기 시대(Stone Age)",value="새 곡괭이로 돌을 채굴하세요",inline=False)
        mincrft_page1.add_field(name="더욱더 좋게(Getting an Upgrade)",value="더 좋은 곡괭이를 만드세요",inline=False)
        mincrft_page1.add_field(name="철이 철철 넘쳐(Acquire Hardware)",value="철 주괴를 제련하세요",inline=False)
        mincrft_page1.add_field(name="차려입기(Suit Up)",value="철 갑옷으로 스스로를 보호하세요",inline=False)
        mincrft_page1.add_field(name="화끈한 화제(Hot Stuff)",value="양동이에 용암을 채우세요",inline=False)
        mincrft_page1.add_field(name="이젠 철 좀 들어라(Isn't It Iron Pick)",value="곡괭이를 개선하세요",inline=False)
        mincrft_page1.add_field(name="저희는 그런 것 받지 않습니다(Not Today, Thank You)",value="방패로 발사체를 튕겨내세요",inline=False)
        mincrft_page1.add_field(name="다이아몬드다!(Diamonds!)",value="다이아몬드를 얻으세요",inline=False)
        mincrft_page1.add_field(name="아이스 버킷 챌린지(Ice Bucket Challenge)",value="흑요석을 얻으세요",inline=False)
        mincrft_page1.add_field(name="­",value="📄 1/2 페이지",inline=False)
        mincrft_page1.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/882161199704330240/Advancement-Minecraft.png")

        mincrft_page2 = discord.Embed(title="Minecraft", description="­", color=0xffdc16)
        mincrft_page2.add_field(name="더 깊은 곳으로(We Need to Go Deeper)",value="네더 차원문을 짓고, 불을 붙여 들어가세요",inline=False)
        mincrft_page2.add_field(name="다이아몬드로 날 감싸줘(Cover Me With Diamonds)",value="다이아몬드 갑옷은 생명을 구합니다.",inline=False)
        mincrft_page2.add_field(name="마법 부여자(Enchanter)",value="마법 부여대로 아이템에 마법을 부여하세요",inline=False)
        mincrft_page2.add_field(name="좀비 의사(Zombie Doctor)",value="좀비 주민을 약화시킨 후 치료하세요",inline=False)
        mincrft_page2.add_field(name="스무고개(Eye Spy)",value="엔더의 눈을 따라가세요",inline=False)
        mincrft_page2.add_field(name="이걸로 끝이야?(The End?)",value="엔드 차원문에 진입하세요",inline=False)
        mincrft_page2.add_field(name="­",value="📄 2/2 페이지",inline=False)
        mincrft_page2.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/882161199704330240/Advancement-Minecraft.png")

        Nether_page1 = discord.Embed(title="네더(Nether)", description="­", color=0xffdc16)
        Nether_page1.add_field(name="네더(Nether)",value="여름옷을 가져오세요",inline=False)
        Nether_page1.add_field(name="천 리 길도 한 걸음(Subspace Bubble)",value="네더를 이용해 오버월드의 7km를 이동하세요",inline=False)
        Nether_page1.add_field(name="끔찍한 요새(A Terrible Fortress)",value="네더 요새 안으로 들어가세요",inline=False)
        Nether_page1.add_field(name="전해지지 않은 러브레터(Return to Sender)",value="화염구로 가스트를 죽이세요",inline=False)
        Nether_page1.add_field(name="포화 속으로(Into Fire)",value="블레이즈의 막대기를 얻으세요",inline=False)
        Nether_page1.add_field(name="으스스한 스켈레톤(Spooky Scary Skeleton)",value="위더 스켈레톤의 해골을 얻으세요",inline=False)
        Nether_page1.add_field(name="쉽지 않은 동행(Uneasy Alliance)",value="네더에서 가스트를 구출해 오버월드로 안전하게 데려온 다음… 죽이세요",inline=False)
        Nether_page1.add_field(name="물약 양조장(Local Brewery)",value="물약을 양조하세요",inline=False)
        Nether_page1.add_field(name="시들어 버린 언덕(Withering Heights)",value="위더를 소환하세요",inline=False)
        Nether_page1.add_field(name="뿅 가는 폭탄주(A Furious Cocktail)",value="모든 물약 효과를 동시에 가지세요",inline=False)
        Nether_page1.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/882460460962693280/Advancement-Nether.png")
        Nether_page1.add_field(name="­",value="📄 1/3 페이지",inline=False)

        Nether_page2 = discord.Embed(title="네더(Nether)", description="­", color=0xffdc16)
        Nether_page2.add_field(name="신호기 꾸리기(Bring Home the Beacon)",value="신호기를 제작하고 설치하세요",inline=False)
        Nether_page2.add_field(name="어쩌다 이 지경까지(How Did We Get Here?)",value="모든 효과를 동시에 가지세요",inline=False)
        Nether_page2.add_field(name="신호자(Beaconator)",value="신호기의 출력을 최대로 만드세요",inline=False)
        Nether_page2.add_field(name="그때가 좋았지(Those Were the Days)",value="보루 잔해에 진입하세요",inline=False)
        Nether_page2.add_field(name="돼지와 전쟁(War Pigs)",value="보루 잔해에 있는 상자에서 노획물을 얻으세요",inline=False)
        Nether_page2.add_field(name="깊이 파묻힌 잔해(Hidden in the Depths)",value="고대 잔해를 얻으세요",inline=False)
        Nether_page2.add_field(name="집으로 이끌려가네(Country Lode, Take Me Home)",value="자석석에 나침반을 사용하세요",inline=False)
        Nether_page2.add_field(name="잔해로 날 감싸줘(Cover Me in Debris)",value="네더라이트 갑옷을 전부 얻으세요",inline=False)
        Nether_page2.add_field(name="누가 양파를 써나?(Who is Cutting Onions?)",value="우는 흑요석을 얻으세요",inline=False)
        Nether_page2.add_field(name='목숨 충전(Not Quite "Nine" Lives)',value="리스폰 정박기를 최대로 충전하세요",inline=False)
        Nether_page2.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/882460460962693280/Advancement-Nether.png")
        Nether_page2.add_field(name="­",value="📄 2/3 페이지",inline=False)

        Nether_page3 = discord.Embed(title="네더(Nether)", description="­", color=0xffdc16)
        Nether_page3.add_field(name="반짝반짝 눈이 부셔(Oh Shiny)",value="금으로 피글린의 주의를 돌리세요",inline=False)
        Nether_page3.add_field(name="두 발 달린 보트(This Boat Has Legs)",value="뒤틀린 균 낚싯대를 들고 스트라이더 위에 탑승하세요",inline=False)
        Nether_page3.add_field(name="화끈한 관광 명소(Hot Tourist Destinations)",value="모든 네더 생물 군계를 탐험하세요",inline=False)
        Nether_page3.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/882460460962693280/Advancement-Nether.png")
        Nether_page3.add_field(name="­",value="📄 3/3 페이지",inline=False)

        Ender_page = discord.Embed(title="엔드(The End)", description="­", color=0xffdc16)
        Ender_page.add_field(name="디 엔드(The End)",value="끝일까요, 아니면 시작일까요?",inline=False)
        Ender_page.add_field(name="엔드 해방(Free the End)",value="행운을 빌어요",inline=False)
        Ender_page.add_field(name="그다음 세대(The Next Generation)",value="드래곤 알을 들어올리세요",inline=False)
        Ender_page.add_field(name="머나먼 휴양지(Remote Getaway)",value="섬에서 탈출하세요",inline=False)
        Ender_page.add_field(name="끝 아녔어?(The End... Again...)",value="엔더 드래곤을 다시 소환하세요",inline=False)
        Ender_page.add_field(name="양치질이 필요해 보이는걸(You Need a Mint)",value="드래곤의 숨결을 유리병에 담으세요",inline=False)
        Ender_page.add_field(name="게임의 끝에서 만난 도시(The City at the End of the Game)",value="들어가 보세요, 뭔 일 일어나겠어요?",inline=False)
        Ender_page.add_field(name="불가능은 없다(Sky's the Limit)",value="겉날개를 찾으세요",inline=False)
        Ender_page.add_field(name="위쪽 공기 좋은데?(Great View From Up Here)",value="설커의 공격을 맞고 블록 50개어치만큼 공중 부양하세요",inline=False)
        Ender_page.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/882494471047114772/Advancement-TheEnd.png")

        Adventure_page1 = discord.Embed(title="모험(Adventure)", description="­", color=0xffdc16)
        Adventure_page1.add_field(name="모험(Adventure)",value="모험, 탐사와 전투",inline=False)
        Adventure_page1.add_field(name="몬스터 사냥꾼(Monster Hunter)",value="적대적 몬스터를 죽이세요",inline=False)
        Adventure_page1.add_field(name="훌륭한 거래군요!(What a Deal!)",value="주민과 거래하세요",inline=False)
        Adventure_page1.add_field(name="달콤한 꿈(Sweet dreams)",value="리스폰 지점을 바꾸세요",inline=False)
        Adventure_page1.add_field(name="준비하시고... 쏘세요!(A Throwaway Joke)",value="무언가를 향해 삼지창을 던지세요\n참고: 가지고 있는 유일한 무기를 내던지는 것은 좋은 생각이 아닙니다.",inline=False)
        Adventure_page1.add_field(name="정조준(Take Aim)",value="화살로 무언가를 맞추세요",inline=False)
        Adventure_page1.add_field(name="몬스터 도감(Monsters Hunted)",value="모든 적대적 몬스터를 하나 이상씩 죽이세요",inline=False)
        Adventure_page1.add_field(name="죽음을 초월한 자(Postmortal)",value="불사의 토템으로 죽음을 기만하세요",inline=False)
        Adventure_page1.add_field(name="도우미 고용(Hired Help)",value="마을 방어를 돕기 위해 철 골렘을 소환하세요",inline=False)
        Adventure_page1.add_field(name="모험의 시간(Adventuring Time)",value="모든 생물군계를 발견하세요",inline=False)
        Adventure_page1.add_field(name="­",value="📄 1/3 페이지",inline=False)
        Adventure_page1.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/882515992314519552/Advancement-Adventure.png")

        Adventure_page2 = discord.Embed(title="모험(Adventure)", description="­", color=0xffdc16)
        Adventure_page2.add_field(name="동에 번쩍 서에 번쩍(Very Very Frightening)",value="주민에게 벼락을 떨어뜨리세요",inline=False)
        Adventure_page2.add_field(name="저격 대결(Sniper Duel)",value="50미터 이상 떨어져 있는 스켈레톤을 화살로 죽이세요",inline=False)
        Adventure_page2.add_field(name="자진 유배(Voluntary Exile)",value="<숨겨진 과제>\n습격 대장을 죽이세요. 당분간 마을에서 떨어져 있는 게 좋을지도 몰라요...",inline=False)
        Adventure_page2.add_field(name="마을의 영웅(Hero of the Village)",value="<숨겨진 과제>\n습격으로부터 마을을 지켜내세요",inline=False)
        Adventure_page2.add_field(name="부러진 화살(Ol' Betsy)",value="쇠뇌를 쏘세요",inline=False)
        Adventure_page2.add_field(name="일전쌍조(Two Birds, One Arrow)",value="관통 화살 한 발로 팬텀 두 마리를 죽이세요",inline=False)
        Adventure_page2.add_field(name="이제 누가 약탈자지?(Who's the Pillager Now?)",value="약탈자에게 똑같은 무기로 앙갚음해 주세요",inline=False)
        Adventure_page2.add_field(name="명사수(Arbalistic)",value="<숨겨진 과제>\n쇠뇌 한 발로 종류가 다른 몹 다섯 마리를 죽이세요",inline=False)
        Adventure_page2.add_field(name="달콤함에 몸을 맡기다(Sticky Situation)",value="꿀 블록을 향해 점프해 낙하를 멈추세요",inline=False)
        Adventure_page2.add_field(name="명중(Bullseye)",value="30미터 이상 떨어진 곳에서 과녁 블록의 정중앙을 맞추세요",inline=False)
        Adventure_page2.add_field(name="­",value="📄 2/3 페이지",inline=False)
        Adventure_page2.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/882515992314519552/Advancement-Adventure.png")

        Adventure_page3 = discord.Embed(title="모험(Adventure)", description="­", color=0xffdc16)
        Adventure_page3.add_field(name="토끼처럼 가볍게(Light as a Rabbit)",value="가루눈 위를 걸으세요... 빠지지 않고요",inline=False)
        Adventure_page3.add_field(name="번개 멈춰!(Surge Protector!)",value="주민의 감전 사고를 화재 없이 막으세요",inline=False)
        Adventure_page3.add_field(name="새인가?(Is it a Bird?)",value="망원경으로 앵무새를 바라보세요",inline=False)
        Adventure_page3.add_field(name="풍선인가?(Is it a Balloon?)",value="망원경으로 가스트를 바라보세요",inline=False)
        Adventure_page3.add_field(name="비행기인가?(Is it a Plane?)",value="망원경으로 엔더 드래곤을 바라보세요",inline=False)
        Adventure_page3.add_field(name="­",value="📄 3/3 페이지",inline=False)
        Adventure_page3.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/882515992314519552/Advancement-Adventure.png")

        Farm_page1 = discord.Embed(title="농사(Husbandry)", description="­", color=0xffdc16)
        Farm_page1.add_field(name="농사(Husbandry)",value="세상은 친구들과 음식으로 가득 차 있어요",inline=False)
        Farm_page1.add_field(name="아기는 어떻게 태어나?(The Parrots and the Bats)",value="동물 두 마리를 교배시키세요",inline=False)
        Farm_page1.add_field(name="인생의 동반자(Best Friends Forever)",value="동물을 길들이세요",inline=False)
        Farm_page1.add_field(name="씨앗이 자라나는 곳(A Seedy Place)",value="씨앗을 심고 자라는 것을 지켜보세요",inline=False)
        Farm_page1.add_field(name="강태공이 세월을 낚듯(Fishy Business)",value="물고기를 잡으세요",inline=False)
        Farm_page1.add_field(name="짝지어주기(Two by Two)",value="모든 동물을 교배시키세요",inline=False)
        Farm_page1.add_field(name="집사 그 자체(A Complete Catalogue)",value="모든 종류의 고양이를 길들이세요!",inline=False)
        Farm_page1.add_field(name="균형 잡힌 식단(A Balanced Diet)",value="먹을 수 있는 것이라면 모두 먹으세요,\n그것이 건강에 좋지 않더라도 말이죠.",inline=False)
        Farm_page1.add_field(name="도를 넘은 전념(Serious Dedication)",value="네더라이트 주괴로 괭이를 강화한 후,\n삶의 선택들을 돌이켜보세요",inline=False)
        Farm_page1.add_field(name="이 대신 잇몸으로(Tactical Fishing)",value="물고기를 잡으세요... 낚싯대 없이요!",inline=False)
        Farm_page1.add_field(name="­",value="📄 1/2 페이지",inline=False)
        Farm_page1.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/882524463193796638/Advancement-Farm.png")

        Farm_page2 = discord.Embed(title="농사(Husbandry)", description="­", color=0xffdc16)
        Farm_page2.add_field(name="벌집을 내 집처럼(Bee Our Guest)",value="꿀벌을 자극하지 않도록 모닥불을 사용해 벌통에 든 꿀을 병에 담으세요",inline=False)
        Farm_page2.add_field(name="한 벌 한 벌 정성껏 모시겠습니다(Total Beelocation)",value="벌 3마리가 들어 있는 벌집을 섬세한 손길을 사용해 옮기세요",inline=False)
        Farm_page2.add_field(name="염소 떴소(Whatever Floats Your Goat!)",value="염소와 함께 보트에 타세요",inline=False)
        Farm_page2.add_field(name="밀랍을 칠하자(Wax on)",value="구리 블록에 벌집 조각을 사용하세요!",inline=False)
        Farm_page2.add_field(name="밀랍을 벗기자(Wax off)",value="구리 블록의 밀랍칠을 벗기세요!",inline=False)
        Farm_page2.add_field(name="귀여운 포식자(The Cutest Predator)",value="양동이로 아홀로틀을 잡으세요",inline=False)
        Farm_page2.add_field(name="우정의 치유력(The Healing Power of Friendship!)",value="아홀로틀과 협력해 싸워 이기세요",inline=False)
        Farm_page2.add_field(name="밝은 말 고운 말(Glow and Behold)",value="표지판의 글자가 빛나게 만드세요",inline=False)
        Farm_page2.add_field(name="­",value="📄 2/2 페이지",inline=False)
        Farm_page2.set_thumbnail(url="https://cdn.discordapp.com/attachments/731471072310067221/882524463193796638/Advancement-Farm.png")

        AdV_Mincrft = ["Minecraft","minecraft","MINECRAFT","마인크래프트","마크"]
        AdV_Nether = ["Nether","nether","NETHER","네더","지옥"]
        AdV_Ender = ["Ender","ender", "ENDER", "엔더", "엔드"]
        AdV_Adventure = ["모험","Adventure", "ADVENTURE"]
        AdV_Farm = ["Husbandry","husbandry","농사"]

        if List == "No Category":
            await ctx.send(embed=AdvCategory)
            return

        elif List in AdV_Mincrft:
            PageList = "2"
            pages = [mincrft_page1, mincrft_page2]
            message = await ctx.send(embed = mincrft_page1)
            await message.add_reaction('◀')
            await message.add_reaction('▶')

        elif List in AdV_Nether:
            PageList = "3"
            pages = [Nether_page1, Nether_page2, Nether_page3]
            message = await ctx.send(embed = Nether_page1)
            await message.add_reaction('⏮')
            await message.add_reaction('◀')
            await message.add_reaction('▶')
            await message.add_reaction('⏭')

        elif List in AdV_Ender:
            PageList = "1"
            message = await ctx.send(embed = Ender_page)

        elif List in AdV_Adventure:
            PageList = "3"
            pages = [Adventure_page1, Adventure_page2, Adventure_page3]
            message = await ctx.send(embed = Adventure_page1)
            await message.add_reaction('⏮')
            await message.add_reaction('◀')
            await message.add_reaction('▶')
            await message.add_reaction('⏭')

        elif List in AdV_Farm:
            PageList = "2"
            pages = [Farm_page1, Farm_page2]
            message = await ctx.send(embed = Farm_page1)
            await message.add_reaction('◀')
            await message.add_reaction('▶')

        else:
            await ctx.send("안됨")
            return

        def check(reaction, user):
            return user == ctx.author

        i = 0
        reaction = None

        while True:
            if str(reaction) == '⏮':
                i = 0
                await message.edit(embed = pages[i])
            elif str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await message.edit(embed = pages[i])
            elif str(reaction) == '▶':
                if PageList == "2":
                    if i < 1:
                        i += 1
                        await message.edit(embed = pages[i])
                else:
                    if i < 2:
                        i += 1
                        await message.edit(embed = pages[i])
            elif str(reaction) == '⏭':
                i = 2
                await message.edit(embed = pages[i])
            
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout = 45.0, check = check)
                await message.remove_reaction(reaction, user)
            except:
                break

        await message.clear_reactions()

def setup(client):
    client.add_cog(minecraft(client))