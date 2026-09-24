import discord
from discord.ext import commands
import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "moderation_config.json")

DEFAULT_CONFIG = {
    "forbidden_channels": [],
    "locked_channels": [],
    "banned_words": [],
    "muted_role_id": None,
    "log_channel_id": None,
    "welcome_channel_id": None
}


def load_config():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
    with open(DATA_PATH, "r") as f:
        return json.load(f)


def save_config(config):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(config, f, indent=2)


def register_set_commands(bot):
    config = load_config()

    # CANAIS PROIBIDOS (membros não podem enviar mensagem)

    @bot.command(name="setforbidden")
    @commands.has_permissions(administrator=True)
    async def setforbidden(ctx: commands.Context, channel: discord.TextChannel = None, action: str = "add"):
        """Adiciona ou remove um canal da lista de canais proibidos.
        Uso: .setforbidden #canal [add/remove]
        """
        channel = channel or ctx.channel
        config = load_config()

        if action.lower() == "add":
            if channel.id not in config["forbidden_channels"]:
                config["forbidden_channels"].append(channel.id)
                save_config(config)
                await ctx.send(f"✅ {channel.mention} adicionado aos canais proibidos. Membros não poderão enviar mensagens.")
            else:
                await ctx.send(f"⚠️ {channel.mention} já está na lista de canais proibidos.")
        elif action.lower() == "remove":
            if channel.id in config["forbidden_channels"]:
                config["forbidden_channels"].remove(channel.id)
                save_config(config)
                await ctx.send(f"✅ {channel.mention} removido dos canais proibidos.")
            else:
                await ctx.send(f"⚠️ {channel.mention} não está na lista de canais proibidos.")
        else:
            await ctx.send("❌ Ação inválida. Use `add` ou `remove`.")

    @bot.command(name="listforbidden")
    @commands.has_permissions(manage_guild=True)
    async def listforbidden(ctx: commands.Context):
        """Lista todos os canais proibidos."""
        config = load_config()
        if not config["forbidden_channels"]:
            await ctx.send("📋 Nenhum canal proibido configurado.")
            return

        channels = []
        for ch_id in config["forbidden_channels"]:
            ch = ctx.guild.get_channel(ch_id)
            channels.append(ch.mention if ch else f"`{ch_id}` (não encontrado)")

        embed = discord.Embed(
            title="🚫 Canais Proibidos",
            description="\n".join(channels) if channels else "Nenhum configurado.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    # CANAIS TRANCADOS (cargos específicos não podem ver/enviar)

    @bot.command(name="setlocked")
    @commands.has_permissions(administrator=True)
    async def setlocked(ctx: commands.Context, channel: discord.TextChannel = None, action: str = "lock"):
        """Trava ou destrava um canal para o cargo @everyone.
        Uso: .setlocked #canal [lock/unlock]
        """
        channel = channel or ctx.channel
        config = load_config()

        if action.lower() == "lock":
            if channel.id not in config["locked_channels"]:
                config["locked_channels"].append(channel.id)
                save_config(config)
                # Remove permissão de enviar mensagens para @everyone
                overwrite = discord.PermissionOverwrite(send_messages=False)
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                await ctx.send(f"🔒 {channel.mention} foi **TRAVADO**. Membros não podem mais enviar mensagens.")
            else:
                await ctx.send(f"⚠️ {channel.mention} já está travado.")
        elif action.lower() == "unlock":
            if channel.id in config["locked_channels"]:
                config["locked_channels"].remove(channel.id)
                save_config(config)
                # Restaura permissão de enviar mensagens para @everyone
                overwrite = discord.PermissionOverwrite(send_messages=True)
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                await ctx.send(f"🔓 {channel.mention} foi **DESBLOQUEADO**.")
            else:
                await ctx.send(f"⚠️ {channel.mention} não está na lista de canais travados.")
        else:
            await ctx.send("❌ Ação inválida. Use `lock` ou `unlock`.")

    @bot.command(name="listlocked")
    @commands.has_permissions(manage_guild=True)
    async def listlocked(ctx: commands.Context):
        """Lista todos os canais travados."""
        config = load_config()
        if not config["locked_channels"]:
            await ctx.send("📋 Nenhum canal travado configurado.")
            return

        channels = []
        for ch_id in config["locked_channels"]:
            ch = ctx.guild.get_channel(ch_id)
            channels.append(ch.mention if ch else f"`{ch_id}` (não encontrado)")

        embed = discord.Embed(
            title="🔒 Canais Travados",
            description="\n".join(channels) if channels else "Nenhum configurado.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

    # PALAVRAS-CHAVE BANIDAS (filtro de conteúdo)

    @bot.command(name="setword")
    @commands.has_permissions(administrator=True)
    async def setword(ctx: commands.Context, palavra: str = None, action: str = "add"):
        """Adiciona ou remove uma palavra da lista de palavras banidas.
        Uso: .setword <palavra> [add/remove]
        """
        if not palavra:
            await ctx.send("❌ Especifique uma palavra. Uso: `.setword <palavra> [add/remove]`")
            return

        config = load_config()
        palavra_lower = palavra.lower()

        if action.lower() == "add":
            if palavra_lower not in config["banned_words"]:
                config["banned_words"].append(palavra_lower)
                save_config(config)
                await ctx.send(f"✅ Palavra `{palavra}` adicionada ao filtro.")
            else:
                await ctx.send(f"⚠️ A palavra `{palavra}` já está na lista.")
        elif action.lower() == "remove":
            if palavra_lower in config["banned_words"]:
                config["banned_words"].remove(palavra_lower)
                save_config(config)
                await ctx.send(f"✅ Palavra `{palavra}` removida do filtro.")
            else:
                await ctx.send(f"⚠️ A palavra `{palavra}` não está na lista.")
        else:
            await ctx.send("❌ Ação inválida. Use `add` ou `remove`.")

    @bot.command(name="listwords")
    @commands.has_permissions(manage_guild=True)
    async def listwords(ctx: commands.Context):
        """Lista todas as palavras banidas."""
        config = load_config()
        if not config["banned_words"]:
            await ctx.send("📋 Nenhuma palavra banida configurada.")
            return

        embed = discord.Embed(
            title="🚫 Palavras Banidas",
            description=", ".join(f"`{w}`" for w in config["banned_words"]),
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    # LISTENERS - Auto-mod

    @bot.listen("on_message")
    async def auto_mod_check(message):
        if message.author.bot or message.guild is None:
            return

        config = load_config()

        # Verifica canal proibido
        if message.channel.id in config["forbidden_channels"]:
            await message.delete()
            try:
                await message.author.send(
                    f"🚫 Você não pode enviar mensagens em {message.channel.mention}."
                )
            except discord.Forbidden:
                pass
            return

        # Verifica canal trancado
        if message.channel.id in config["locked_channels"]:
            await message.delete()
            return

        # Verifica palavras banidas
        if config["banned_words"]:
            content_lower = message.content.lower()
            for word in config["banned_words"]:
                if word in content_lower:
                    await message.delete()
                    warn_msg = await message.channel.send(
                        f"⚠️ {message.author.mention}, sua mensagem continha uma palavra proibida e foi removida.",
                        delete_after=10
                    )
                    try:
                        await message.author.send(
                            f"🚫 Sua mensagem em {message.channel.mention} foi removida por conter uma palavra proibida."
                        )
                    except discord.Forbidden:
                        pass
                    break


async def setup(bot):
    register_set_commands(bot)
