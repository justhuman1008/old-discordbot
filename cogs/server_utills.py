from discord.ext import commands
import discord
from discord.utils import get
from discord.utils import *

is_it_me = 512166620463104004

class server_utills(commands.Cog):

    def __init__(self, client):
        self.bot = client
        self.stopcodes = 0

    @commands.command(aliases=['서버 관리', '서버관리'])
    async def serverhelp(self, ctx):
        embed = discord.Embed(title="서버 관리용 명령어", description="­봇의 접두사는 `!`입니다.", color=0xffdc16)
        embed.add_field(name=':small_blue_diamond:'+"!서버정보", value="서버에 대한 정보를 출력합니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!추방 `{멘션}`", value="멘션한 유저를 추방합니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!차단 `{멘션}`", value="`멘션한 유저를 차단합니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!차단해제 `닉네임#태그`", value="해당 유저를 차단해제합니다.", inline=False)
        embed.add_field(name=':small_blue_diamond:'+"!청소 `{수}`", value="{수}만큼 메시지를 삭제합니다.", inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/731471072310067221/777102022771343370/cust.png')
        await ctx.send(embed = embed)



    @commands.command(aliases=['서버정보', '서버 정보'])
    async def guildinfo(self, ctx):
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

        # Embed
        guild_info = discord.Embed(title=f"{current_guild.name}", colour=0xffdc16)
        guild_info.add_field(name="서버 ID", value=f"`{current_guild.id}`", inline=True)
        guild_info.add_field(name="서버 주인", value=f"`{current_guild.owner}`", inline=True)
        guild_info.add_field(name="­", value="­", inline=True)
        guild_info.add_field(name="텍스트 채널 갯수", value=f"`{len(current_guild.text_channels)}개`", inline=True)
        guild_info.add_field(name="음성 통화방 갯수", value=f"`{len(current_guild.voice_channels)}개`", inline=True)
        guild_info.add_field(name="­", value="­", inline=True)
        guild_info.add_field(name="유저", value=f"`인원 총합: {current_guild.member_count}\n온라인 유저: {member_statuses['online']}`", inline=True)
        guild_info.add_field(name="서버 보안 수준", value=f"`{safety_settings['verification level']}`", inline=True)
        guild_info.add_field(name = '부스트 레벨', value = f"`{current_guild.premium_tier}`", inline =True)
        guild_info.add_field(name="서버 생성 일자", value=f"`{current_guild.created_at}`", inline=True)
        guild_info.add_field(name="서버 위치", value=f"`{current_guild.region}`", inline=True)
        guild_info.set_thumbnail(url=current_guild.icon_url)
        await ctx.send(embed=guild_info)



    @commands.command(aliases=['추방', '킥'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.User=None, reason =None):
        if reason == None:
            reason = "추방사유 미작성됨"
        if member == None:
            await ctx.send(embed=discord.Embed(title="추방할 유저를 멘션해주세요", description="!추방 {멘션}", color=0xf8e71c))
            return
        await ctx.guild.kick(member, reason=reason)
        await ctx.channel.send(f"{member.mention}님을 추방하였습니다.\n사유 : {reason}")


    @commands.command(aliases=['차단', '밴'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.User=None, reason =None):
        if reason == None:
            reason = "차단사유 미작성됨"
        if member == None:
            await ctx.send(embed=discord.Embed(title="추방할 유저를 멘션해주세요", description="!차단 {멘션}", color=0xf8e71c))
            return
        await ctx.guild.ban(member, reason=reason)
        await ctx.channel.send(f"{member.mention}님을 차단하였습니다.\n사유 : {reason}")



    @commands.command(aliases=['차단해제', '언밴'])
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):

        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention}님을 차단해제하였습니다.')
                return

    @commands.command(aliases=['내정보'])
    async def myinfo(self, ctx):
        user_info = discord.Embed(title=ctx.author.name+"#"+ctx.author.discriminator, colour=0xffdc16)
        user_info.add_field(name="별명", value="`"+ctx.author.display_name+"`", inline=True)
        user_info.add_field(name="유저 ID", value="`"+str(ctx.author.id)+"`", inline=True)
        user_info.add_field(name="역할", value="`"+str(ctx.author.top_role)+"`", inline=True)
        user_info.add_field(name="계정 생성일", value="`"+str(ctx.author.created_at.strftime("%Y %B %d %a"))+"`", inline=True)
        user_info.add_field(name="서버 참가일", value="`"+str(ctx.author.joined_at.strftime("%Y %B %d %a"))+"`", inline=True)
        user_info.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=user_info)

def setup(client):
    client.add_cog(server_utills(client))