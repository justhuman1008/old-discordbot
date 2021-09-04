import discord
from discord.ext import commands
from discord.utils import get
from discord.utils import *



class server_utills(commands.Cog):

    def __init__(self, client):
        self.bot = client
        self.stopcodes = 0

    @commands.command(aliases=['서버정보', '서버 정보'])
    async def _guildinfo(self, ctx):
        print(f'디스코드 서버에 대한 정보를 불러옵니다.')
        current_guild: discord.Guild = ctx.guild
        member_statuses = {
            "online": 0,
            "idle": 0,
            "dnd": 0,
            "offline/invisible": 0
        }

        safety_settings = {
            "2FA Setting": current_guild.mfa_level,
            "verification level": current_guild.verification_level
        }


        # 온라인 유저 확인
        for member in current_guild.members:
            if str(member.status) == "online":
                member_statuses["online"] += 1
        print(f'-온라인 유저수 확인 완료')

        # 보안 레벨
        if safety_settings['verification level'] == discord.VerificationLevel.none:
            safety_settings['verification level'] = "제한 없음"
        elif safety_settings['verification level'] == discord.VerificationLevel.low:
            safety_settings['verification level'] = "이메일 인증 필요"
        elif safety_settings['verification level'] == discord.VerificationLevel.medium:
            safety_settings['verification level'] = "가입후 5분 대기 필요"
        elif safety_settings['verification level'] == discord.VerificationLevel.high or safety_settings['verification level'] == discord.VerificationLevel.table_flip:
            safety_settings['verification level'] = "참여후 10분 대기 필요"
        elif safety_settings['verification level'] == discord.VerificationLevel.extreme or safety_settings['verification level'] == discord.VerificationLevel.double_table_flip:
            safety_settings['verification level'] = "휴대폰 인증 필요"
        print(f'-서버의 보안 레벨 확인 완료')

        # Embed
        roles = ctx.guild.roles
        guild_info = discord.Embed(title=f"{current_guild.name}", colour=0xffdc16)
        guild_info.add_field(name="서버 ID", value=f"`{current_guild.id}`", inline=True)
        guild_info.add_field(name="서버 주인", value=f"`{current_guild.owner}`", inline=True)
        guild_info.add_field(name='서버 최고 역할', value=f'{roles[-1].mention}', inline=True)
        guild_info.add_field(name="텍스트 채널 ", value=f"`{len(current_guild.text_channels)}개`", inline=True)
        guild_info.add_field(name="음성 통화방 ", value=f"`{len(current_guild.voice_channels)}개`", inline=True)
        guild_info.add_field(name="카테고리 ", value=f"`{str(len(ctx.guild.categories))}개`", inline=True)
        guild_info.add_field(name="유저", value=f"`인원 총합: {current_guild.member_count}명\n온라인 유저: {member_statuses['online']}명`", inline=True)
        guild_info.add_field(name='역할수', value="`"+str(len(ctx.guild.roles)) + '개`', inline=True)
        guild_info.add_field(name="이모지 수", value =f'`{len(ctx.guild.emojis)}개`', inline=True)
        guild_info.add_field(name="서버 보안 수준", value=f"`{safety_settings['verification level']}`", inline=True)
        guild_info.add_field(name ='부스트 레벨', value = f"`{current_guild.premium_tier}`", inline =True)
        guild_info.add_field(name="서버 생성 일자", value=f'`{ctx.guild.created_at.strftime("%Y-%m-%d %I")}`', inline=True)
        guild_info.add_field(name="서버 위치", value=f"`{current_guild.region}`", inline=True)
        guild_info.set_thumbnail(url=current_guild.icon_url)
        await ctx.send(embed=guild_info)
        print(f'디스코드 서버 정보를 성공적으로 전송하였습니다.')



    @commands.command(aliases=['추방', '킥'],usage="!추방 `{멘션}`")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.User=None, reason =None):
        if reason == None:
            reason = "추방사유 미작성됨"
        if member == None:
            await ctx.send(embed=discord.Embed(title="추방할 유저를 멘션해주세요", description="!추방 {멘션}", color=0xf8e71c))
            return
        await ctx.guild.kick(member, reason=reason)
        await ctx.channel.send(f"> {member.mention}님을 추방하였습니다.\n> 사유 : {reason}")
        print(f"봇이 {ctx.author}님의 명령을 받아 {member.mention}님을 추방하였습니다.\n> 사유 : {reason}")


    @commands.command(aliases=['차단', '밴'],usage="!차단 `{멘션}`")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.User=None, reason =None):
        if reason == None:
            reason = "차단사유 미작성됨"
        if member == None:
            await ctx.send(embed=discord.Embed(title="추방할 유저를 멘션해주세요", description="!차단 {멘션}", color=0xf8e71c))
            return
        await ctx.guild.ban(member, reason=reason)
        await ctx.channel.send(f"> {member.mention}님을 차단하였습니다.\n> 사유 : {reason}")
        print(f"봇이 {ctx.author}님의 명령을 받아 {member.mention}님을 차단하였습니다.\n> 사유 : {reason}")

    @commands.command(aliases=['차단해제', '언밴'],usage="!차단해제 `{닉네임#태그}`") #Com5
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):

        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'> {user.mention}님을 차단해제하였습니다.')
                print(f"봇이 {ctx.author}님의 명령을 받아 {member.mention}님을 차단해제하였습니다.")
                return

    @commands.command(aliases=['내정보'])
    async def _myinfo(self, ctx):
        user_info = discord.Embed(title=ctx.author.name+"#"+ctx.author.discriminator, colour=0xffdc16)
        user_info.add_field(name="별명", value="`"+ctx.author.display_name+"`", inline=True)
        user_info.add_field(name="유저 ID", value="`"+str(ctx.author.id)+"`", inline=True)
        user_info.add_field(name="역할", value="`"+str(ctx.author.top_role)+"`", inline=True)
        user_info.add_field(name="계정 생성일", value="`"+str(ctx.author.created_at.strftime("%Y %B %d %a"))+"`", inline=True)
        user_info.add_field(name="서버 참가일", value="`"+str(ctx.author.joined_at.strftime("%Y %B %d %a"))+"`", inline=True)
        user_info.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=user_info)

    @commands.command(aliases=['역할추가', '역할생성'])
    @commands.has_permissions(manage_roles=True)
    async def _create_role(self, ctx, role):
	    await ctx.guild.create_role(name=role,colour=discord.Colour(0xf8e71c))
	    await ctx.send(embed=discord.Embed(title=f"역할 `{role}`이(가) 생성되었습니다.", color=0xf8e71c))

    @commands.command(aliases=['초대링크', '서버초대'],pass_context=True)
    @commands.has_permissions(create_instant_invite=True)
    async def _create_invite(self, ctx, uses=10):
        invitelink = await ctx.channel.create_invite(max_uses=uses, unique=True)
        await ctx.send(f'> **{ctx.guild}** 서버의 초대링크를 생성하였습니다(`{uses}회 제한`)\n> {invitelink}')


    @commands.command(aliases=['슬로우', '슬로우모드'])
    @commands.has_permissions(manage_channels=True)
    async def _slowmode(self, ctx, num: int, chan: discord.TextChannel = None):
        if chan is None:
            chan = ctx.message.channel
        if num < 0:
            await ctx.send(embed=discord.Embed(title="0보다 큰 수를 입력해주세요.", color=0xf8e71c))
            return

        await chan.edit(slowmode_delay=num)
        if num == 0:
            await ctx.send(embed=discord.Embed(title=':clock1:'+" 슬로우모드가 해제되었습니다.", color=0xf8e71c))
            return
        await ctx.send(embed=discord.Embed(title=':clock1:'+f" 이 채널에 {num}초 슬로우모드가 적용되었습니다.", color=0xf8e71c))

    @commands.command(aliases=['채널생성','채팅채널생성'],usage="!채널생성 `{채널명}`")
    @commands.has_permissions(manage_channels=True)
    async def _mchle(self, ctx, channel):
        await ctx.guild.create_text_channel(channel)
        await ctx.send(embed=discord.Embed(title="`"+channel+"` 채널을 생성하였습니다.", color=0xf8e71c))
        await ctx.set_permissions('muted', overwrite=None)
        return

    @commands.command(aliases=['음성채널생성', '통화방생성'],usage="!음성채널생성 `{채널명}`")
    @commands.has_permissions(manage_channels=True)
    async def _mVchle(self, ctx, channel):
        await ctx.guild.create_voice_channel(channel)
        await ctx.send(embed=discord.Embed(title="`"+channel+"` 채널을 생성하였습니다.", color=0xf8e71c))
        return

    @commands.command(aliases=['카테고리생성'],usage="!카테고리생성 `{카테고리명}`")
    @commands.has_permissions(manage_channels=True)
    async def create_category(self, ctx, name):
        await ctx.guild.create_category(name)
        await ctx.send(embed=discord.Embed(title="`"+name+"` 카테고리를 생성하였습니다.", color=0xf8e71c))
        return



def setup(client):
    client.add_cog(server_utills(client))