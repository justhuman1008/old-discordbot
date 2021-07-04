from discord.ext import commands
import discord

is_it_me = 512166620463104004

class server_utills(commands.Cog):

    def __init__(self, client):
        self.bot = client
        self.stopcodes = 0





    @commands.command()
    async def guildinfo(self, ctx):
        current_guild: discord.Guild = ctx.guild
        member_counts = {
            "bot count": 0,
            "human count": 0
        }
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
        guild_info.add_field(name="­", value="­", inline=True)
        guild_info.add_field(name="서버 생성 일자", value=f"`{current_guild.created_at}`", inline=True)
        guild_info.add_field(name="서버 위치", value=f"`{current_guild.region}`", inline=True)
        guild_info.set_thumbnail(url=current_guild.icon_url)
        await ctx.send(embed=guild_info)



    @commands.command(aliases=['추방', '킥'])
    @commands.has_permissions(manage_guild=True)
    async def kick(self, ctx, member:discord.User=None, reason =None):
        if reason == None:
            reason = "추방사유 미작성됨"
        if member == None:
            await ctx.send(embed=discord.Embed(title="추방할 유저를 멘션해주세요", description="!추방 {멘션}", color=0xf8e71c))
        await ctx.guild.kick(member, reason=reason)
        await ctx.channel.send(f"{member.mention}님을 추방하였습니다.\n사유 : {reason}")


    
    @commands.command(aliases=['차단', '밴'])
    @commands.has_permissions(manage_guild=True)
    async def ban(self, ctx, member:discord.User=None, reason =None):
        if reason == None:
            reason = "차단사유 미작성됨"
        if member == None:
            await ctx.send(embed=discord.Embed(title="추방할 유저를 멘션해주세요", description="!차단 {멘션}", color=0xf8e71c))
        await ctx.guild.ban(member, reason=reason)
        await ctx.channel.send(f"{member.mention}님을 차단하였습니다.\n사유 : {reason}")



    @commands.command(aliases=['차단해제', '언밴'])
    @commands.has_permissions(manage_guild=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention}님을 차단해제하였습니다.')
                return



def setup(client):
    client.add_cog(server_utills(client))