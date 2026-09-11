from discord.ext import commands
import discord


def register_commands(bot):
    @bot.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, motivo=None):
        bot_member = ctx.guild.me

        if not bot_member.guild_permissions.ban_members:
            await ctx.send("Nao tenho permissao para banir membros.")
            return

        if member == ctx.guild.owner:
            await ctx.send("Nao consigo banir o dono do servidor.")
            return

        if member.top_role >= bot_member.top_role:
            await ctx.send(
                f"Nao consigo banir {member.mention}: o cargo dele e igual ou acima do meu."
            )
            return

        try:
            await member.ban(reason=motivo)
        except discord.Forbidden:
            await ctx.send("O Discord recusou o ban. Verifique minha permissao e a hierarquia de cargos.")
            return

        await ctx.send(f"{member} foi banido.")

    @bot.command()
    async def clear(ctx: commands.Context, quantidade: int):
        await ctx.channel.purge(limit=quantidade + 1)

    @bot.command()
    async def kick(ctx, member: discord.Member, *, motivo=None):
        await member.kick(reason=motivo)
        await ctx.send(f"{member} foi expulso.")

    @bot.command()
    async def unban(ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention} foi desbanido.")
                return

        await ctx.send(f"Usuário {member} não encontrado na lista de banidos.")

