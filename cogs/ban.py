from discord.ext import commands
import discord

is_it_me = 512166620463104004

class ban(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.stopcodes = 0


    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def kick(self, ctx, member:discord.User=None, reason =None):
        if reason == None:
            reason = "추방사유 미작성됨"
        await ctx.guild.kick(member, reason=reason)
        await ctx.channel.send(f"{member.mention}님을 추방하였습니다.\n사유 : {reason}")


    
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def ban(self, ctx, member:discord.User=None, reason =None):
        if reason == None:
            reason = "차단사유 미작성됨"
        await ctx.guild.ban(member, reason=reason)
        await ctx.channel.send(f"{member.mention}님을 차단하였습니다.\n사유 : {reason}")



    @commands.command()
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


def setup(bot):
    bot.add_cog(ban(bot))