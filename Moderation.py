from discord.ext import commands
import discord

def register_commands(bot):
    @bot.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, motivo=None):
        bot_member = ctx.guild.me
        if not bot_member.guild_permissions.ban_members or member == ctx.guild.owner or member.top_role >= bot_member.top_role:
            await ctx.send("Não tenho permissão ou hierarquia para banir este usuário.")
            return
        try:
            await member.ban(reason=motivo)
            await ctx.send(f"{member} foi banido.")
        except discord.Forbidden:
            await ctx.send("Erro de permissão do Discord.")

    @bot.command()
    async def clear(ctx: commands.Context, quantidade: int):
        await ctx.channel.purge(limit=quantidade + 1)

    @bot.command()
    async def kick(ctx, member: discord.Member, *, motivo=None):
        await member.kick(reason=motivo)
        await ctx.send(f"{member} foi expulso.")

    @bot.command()
    async def unban(ctx, *, user_id: str):
        try:
            user = await bot.fetch_user(int(user_id))
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} foi desbanido.")
        except Exception:
            await ctx.send(f"Não consegui encontrar o usuário com ID {user_id}.")