import discord 
from discord.ext import commands
import os
import random
from dotenv import load_dotenv
load_dotenv()
import asyncio
import io
import aiohttp
from Moderation import register_commands

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)
register_commands(bot)

FORBIDDEN_CHANNEL_ID = 1518314179617095701

from Moderation import register_commands
from slashCommands import register_slash_commands # <--- Adicione este import

bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

register_commands(bot)         # Registro de comandos de prefixo (.)
register_slash_commands(bot)   # Registro de comandos slash (/) <--- Adicione esta linha

@bot.event
async def setup_hook():
    synced_commands = await bot.tree.sync()
    print(f"Sincronizados {len(synced_commands)} comandos slash.")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.command()
async def oi(ctx:commands.Context):
    usuario = ctx.author
    await ctx.send (f"Ola, {ctx.author.mention}!")
 
@bot.command()
async def help(ctx:commands.Context):
    await ctx.send(f"Comandos disponíveis: .oi, .help, .mommy, .tiger, .erika, .maho, .jenzimibra, .ghost, .randola, .resenha, .sexo, .tigerE, .isa, .gaymeter, .boris, .pergunta, .lembrete, .echo, .clear, .kick, .unban")

@bot.command()
async def tiger(ctx:commands.Context):
    await ctx.send("https://www.flamesofwar.com/Portals/0/all_images/Briefings/NorthAfrica/Tunisian-Tigers-01.jpg")

@bot.command(name="erika")
async def erika(ctx: commands.Context):
    await ctx.send(
        "https://media.discordapp.net/attachments/1443943422246391919/1498066065153069146/IMG-20260421-WA0024.jpg?ex=69efce3e&is=69ee7cbe&hm=b293c846869edd0f7e959ab4f4239a51782dd18f6e1146"
    )

@bot.command(name="maho")
async def maho(ctx:  commands.Context):
    await ctx.send("https://media.discordapp.net/attachments/1443943422246391919/1498066065656250461/20260421_183600.jpg?ex=69efce3e&is=69ee7cbe&hm=6f71ab75860f2240ec531e4610bffe6faf2361ecefbae2b")

@bot.command(name="ghost")
async def ghost(ctx:  commands.Context):
    await ctx.send("Vai tomar no cu, @mr.ghostzer0")

@bot.command()
async def randola(ctx:commands.Context):
    await ctx.send("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRA3Gf1NRv1z_3KNwA1iLxv3YddUpIf6MHrsQ&s")

@bot.command()
async def resenha(ctx:commands.Context):
    await ctx.send("https://packaged-media.redd.it/jyln4c8i1w2g1/pb/m2-res_504p.mp4?m=DASHPlaylist.mpd&var=sgpssan&v=1&e=1777258800&s=14fce1da54a5e7d5274ecf85200ce8386d93c821")

@bot.command()
async def sexo(ctx:commands.Context):
    await ctx.send("https://cdn.discordapp.com/attachments/1443943421088895097/1498095460760682637/bixo_aranha_gritando_sexo_por_16_segundoskkkkkkk.mp4?ex=69efe99f&is=69ee981f&hm=f9c9ce9d394b612b")

@bot.command()
async def tigerE(ctx:commands.Context):
    await ctx.send("https://cdn.discordapp.com/attachments/1443943419868352715/1498141277898932224/Screenshot_20260426_225742_Discord.jpg?ex=69f0144a&is=69eec2ca&hm=ee3a5c55f88f78d63fa0e3084caa4d")

@bot.command()
async def gaymeter(ctx:commands.Context):
    await ctx.send(f"O {ctx.author.mention} é {random.randint(0, 100)}% gay.")

@bot.command()
async def boris(ctx:commands.Context):
    await ctx.send("https://cdn.discordapp.com/attachments/1443943421088895097/1498153371775930448/ssstik.io_pnd1st_1777257934952.mp4?ex=69f01f8e&is=69eece0e&hm=705e38d8717bb646ee495a31a6531eddbb")

@bot.command()
async def pergunta(ctx:commands.Context):
    await ctx.send(f"{random.choice(['sim', 'não', 'talvez'])}.")

@bot.command()
async def echo(ctx:commands.Context, *, mensagem: str):
    await ctx.send(mensagem)
    await ctx.message.delete()

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Programando em C#", url = "https://open.spotify.com/playlist/1pKl90hswFVzOmX2186vOZ?si=930bdd21377e4d50"))

@bot.listen('on_message')
async def auto_ban_forbidden_channel(message):
    if message.author.bot or message.guild is None:
        return

    if message.channel.id != FORBIDDEN_CHANNEL_ID:
        return

    bot_member = message.guild.me
    if not bot_member.guild_permissions.ban_members:
        await message.channel.send("Nao tenho permissao para banir membros.")
        return

    member = message.author
    if member.top_role >= bot_member.top_role:
        await message.channel.send(f"Nao consigo banir {member.mention}: cargo igual ou acima do meu.")
        return

    await member.ban(reason="Auto-ban por enviar mensagem no canal proibido")
    await message.channel.send(f"{member} foi banido.")
@bot.command()
async def export(ctx:commands.Context):
    channel = ctx.channel
    limit = 100000
    messages = [message async for message in channel.history(limit=limit, oldest_first=True)]

    output = io.StringIO()
    for msg in messages:
        timestamp = msg.created_at.isoformat()
        author = msg.author
        content = msg.content
        output.write(f"[{timestamp}] {author}: {content}\n")

    output.seek(0)
    await ctx.send(file=discord.File(fp=output, filename=f"history_{channel.id}.txt"))

@bot.command()
async def coruja(ctx):
    if not PEXELS_API_KEY:
        await ctx.send("A chave da API do Pexels não está configurada.")
        return

    url = "https://api.pexels.com/v1/search"

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    params = {
        "query": "owl",
        "per_page": 20,
        "locale": "en-US"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:

            if response.status != 200:
                await ctx.send("Deu merda ao consultar o Pexels 💀")
                return

            data = await response.json()

    fotos = data.get("photos", [])

    if not fotos:
        await ctx.send("Não achei nenhuma coruja 🦉")
        return

    foto = random.choice(fotos)

    embed = discord.Embed(
        title="🦉 Coruja encontrada!",
        url=foto["url"]
    )

    embed.set_image(url=foto["src"]["large"])

    embed.set_footer(
        text=f"Foto por {foto['photographer']} • Pexels"
    )

    await ctx.send(embed=embed)

@bot.tree.command(name="teste", description="Comando de teste")
async def teste(interaction: discord.Interaction):
    await interaction.response.send_message("Angry Birds")

bot.run(os.getenv('DISCORD_TOKEN'))
