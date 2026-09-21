import discord 
from discord.ext import commands
import os
import random
import asyncio
import io
import aiohttp
from dotenv import load_dotenv
from klippyApi import get_random_gif

from Moderation import register_commands
from SetModeration import register_set_commands
from slashCommands import register_slash_commands

load_dotenv()

# Configurações Globais
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
FORBIDDEN_CHANNEL_ID = 1518314179617095701

# Configuração do Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

# Registro de Módulos
register_commands(bot)
register_set_commands(bot)
register_slash_commands(bot)

@bot.event
async def setup_hook():
    """Evento executado antes do bot ligar completamente. Ideal para Sync de Slash Commands."""
    try:
        synced = await bot.tree.sync()
        print(f"✅ Sincronizados {len(synced)} comandos slash globalmente.")
    except Exception as e:
        print(f"❌ Erro ao sincronizar slash commands: {e}")

@bot.event
async def on_ready():
    print(f'🚀 Silence online como {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(activity=discord.Streaming(
        name="Eu nâo quero trabalhar!!!", 
        url="https://open.spotify.com/playlist/1pKl90hswFVzOmX2186vOZ?si=93bdd21377e4d50"
    ))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

# --- COMANDOS DE PREFIXO (.) ---

@bot.command()
async def oi(ctx: commands.Context):
    await ctx.send(f"Olá, {ctx.author.mention}!")

@bot.command()
async def help(ctx: commands.Context):
    msg = (
        "**📚 Comandos Disponíveis:**\n"
        "`.oi`, `.help`, `.tiger`, `.erika`, `.maho`, `.ghost`, `.randola`, `.resenha`, "
        "`.sexo`, `.tigerE`, `.gaymeter`, `.boris`, `.pergunta`, `.echo`, `.export`, "
        "`.coruja`, `.ban`, `.clear`, `.kick`,`.unban`\n\n"
        "💡 *Dica: Use / para ver a lista de Slash Commands modernos!*"
    )
    await ctx.send(msg)

@bot.command()
async def tiger(ctx: commands.Context):
    await ctx.send("https://www.flamesofwar.com/Portals/0/all_images/Briefings/NorthAfrica/Tunisian-Tigers-01.jpg")

@bot.command(name="erika")
async def erika(ctx: commands.Context):
    await ctx.send("https://media.discordapp.net/attachments/1443943422246391919/1498066065153069146/IMG-20260421-WA0024.jpg")

@bot.command(name="maho")
async def maho(ctx: commands.Context):
    await ctx.send("https://media.discordapp.net/attachments/1443943422246391919/1498066065656250461/20260421_183600.jpg")

@bot.command(name="ghost")
async def ghost(ctx: commands.Context):
    await ctx.send("Vai tomar no cu, @mr.ghostzer0")

@bot.command()
async def randola(ctx: commands.Context):
    await ctx.send("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRA3Gf1NRv1z_3KNwA1iLxv3Y_ la a l l")

@bot.command()
async def resenha(ctx: commands.Context):
    await ctx.send("https://packaged-media.redd.it/jyln4c8i1w2g1/pb/m2-res_504p.mp4")

@bot.command()
async def sexo(ctx: commands.Context):
    await ctx.send("https://cdn.discordapp.com/attachments/1443943421088895097/1498095460760682637/bixo_aranha_gritando_sexo_por_16_segundoskkkkkkk.mp4")

@bot.command()
async def tigerE(ctx: commands.Context):
    await ctx.send("https://cdn.discordapp.com/attachments/1443943419868352715/1498141277898932224/Screenshot_20260426_225742_Discord.jpg")

@bot.command()
async def gaymeter(ctx: commands.Context):
    await ctx.send(f"O {ctx.author.mention} é {random.randint(0, 100)}% gay.")

@bot.command()
async def boris(ctx: commands.Context):
    await ctx.send("https://cdn.discordapp.com/attachments/1443943421088895097/1498153371775930448/ssstik.io_pnd1st_1777257934952.mp4")

@bot.command()
async def pergunta(ctx: commands.Context):
    await ctx.send(random.choice(['sim', 'não', 'talvez']))

@bot.command()
async def echo(ctx: commands.Context, *, mensagem: str):
    await ctx.send(mensagem)
    await ctx.message.delete()

@bot.command()
async def export(ctx: commands.Context):
    channel = ctx.channel
    messages = [msg async for msg in channel.history(limit=100000, oldest_first=True)]
    output = io.StringIO()
    for msg in messages:
        output.write(f"[{msg.created_at.isoformat()}] {msg.author}: {msg.content}\n")
    output.seek(0)
    await ctx.send(file=discord.File(fp=output, filename=f"history_{channel.id}.txt"))

@bot.command()
async def setregras(ctx: commands.Context):
    """Publica as regras oficiais do servidor em um Embed Profissional."""
    neon_magenta = discord.Color.from_rgb(255, 0, 255)
    image_path = "C:/Users/gensh/AppData/Local/hermes/cache/images/img_c0f641824f80.webp"
    
    embed = discord.Embed(
        title="📜 CÓDIGO DE CONDUTA | NEW EMPIRE",
        description="*A conformidade com estas diretrizes garante a estabilidade e a excelência do nosso ecossistema. A ignorância das regras não justifica a sua infração.*",
        color=neon_magenta
    )
    
    embed.set_image(url="attachment://regras_banner.webp")
    
    embed.add_field(
        name="🤝 1. CONVIVÊNCIA E RESPEITO",
        value="• É terminantemente proibido qualquer forma de discriminação, assédio ou toxicidade.\n• Debates são encorajados; ataques pessoais são proibidos.\n• O respeito mútuo é a base da nossa comunidade.",
        inline=False
    )
    
    embed.add_field(
        name="📂 2. ORGANIZAÇÃO E CONTEÚDO",
        value="• Utilize os canais adequados para cada assunto (Tech, Música, Social).\n• Evite spam, flood ou o envio excessivo de mensagens irrelevantes.\n• Proibido o envio de conteúdo NSFW ou material ilegal.",
        inline=False
    )
    
    embed.add_field(
        name="🛡️ 3. SEGURANÇA E PRIVACIDADE",
        value="• Não compartilhe informações pessoais (doxxing) de terceiros.\n• Proibido o envio de links suspeitos, malwares ou tentativas de phishing.\n• Respeite a privacidade dos membros e da administração.",
        inline=False
    )
    
    embed.add_field(
        name="👑 4. GOVERNANÇA E MODERAÇÃO",
        value="• As decisões da Administração são finais e soberanas.\n• Sanções (Mute/Ban) serão aplicadas conforme a gravidade da infração.\n• Para suporte ou denúncias, utilize os canais oficiais de atendimento.",
        inline=False
    )
    embed.add_field(
        name="🌐 DIRETRIZES GLOBAIS",
        value="Além destas normas, todos os membros devem seguir rigorosamente as [Diretrizes da Comunidade do Discord](https://discord.com/guidelines).",
        inline=False
    )
    
    embed.set_footer(text="New Empire Administration • Versão 2.0", icon_url=bot.user.avatar.url if bot.user.avatar else None)
    
    file = discord.File(image_path, filename="regras_banner.webp")
    await ctx.send(file=file, embed=embed)
    await ctx.message.delete()

@bot.command()
async def coruja(ctx):
    if not PEXELS_API_KEY:
        await ctx.send("A chave da API do Pexels não está configurada.")
        return
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.pexels.com/v1/search", 
                               headers={"Authorization": PEXELS_API_KEY}, 
                               params={"query": "owl", "per_page": 20}) as resp:
            if resp.status != 200:
                await ctx.send("Deu merda ao consultar o Pexels 💀")
                return
            data = await resp.json()
            fotos = data.get("photos", [])
            if not fotos:
                await ctx.send("Não achei nenhuma coruja 🦉")
                return
            foto = random.choice(fotos)
            embed = discord.Embed(title="🦉 Coruja encontrada!", url=foto["url"])
            embed.set_image(url=foto["src"]["large"])
            embed.set_footer(text=f"Foto por {foto['photographer']} • Pexels")
            await ctx.send(embed=embed)

@bot.listen('on_message')
async def auto_ban_forbidden_channel(message):
    if message.author.bot or message.guild is None or message.channel.id != FORBIDDEN_CHANNEL_ID:
        return
    bot_member = message.guild.me
    if not bot_member.guild_permissions.ban_members or message.author.top_role >= bot_member.top_role:
        return
    await message.author.ban(reason="Auto-ban por enviar mensagem no canal proibido")
    await message.channel.send(f"{message.author} foi banido.")

@bot.command()
async def beijar(ctx: commands.Context, member: discord.Member):
    gif = await get_random_gif("kissing anime")
    if gif:
        embed = discord.Embed(description=f"{ctx.author.mention} beijou {member.mention}! 💋")
        embed.set_image(url=gif)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{ctx.author.mention} tentou beijar {member.mention}, mas levou um vácuo! 💨")

@bot.command(name="lamber", aliases=["lick"])
async def lamber(ctx: commands.Context, member: discord.Member):
    gif = await get_random_gif("anime lick")
    if gif:
        embed = discord.Embed(description=f"{ctx.author.mention} lambeu {member.mention}! 😋")
        embed.set_image(url=gif)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{ctx.author.mention} tentou lamber {member.mention}, mas a língua escorregou! 👅")

@bot.command(name="matar", aliases=["kill"])
async def matar(ctx: commands.Context, member: discord.Member):
    gif = await get_random_gif("anime kill")
    if gif:
        embed = discord.Embed(description=f"{ctx.author.mention} matou {member.mention}! 💀")
        embed.set_image(url=gif)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{ctx.author.mention} tentou matar {member.mention}, mas não conseguiu! 🛡️")

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))