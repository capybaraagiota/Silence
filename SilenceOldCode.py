
from enum import member

import discord 
from discord import message
from discord.ext import commands
import os
import random
from dotenv import load_dotenv
load_dotenv()
import datetime
import asyncio
import io
import json
from tigerAi import run_tiger_query

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

bot.remove_command('help')

LEVELS_FILE = "levels.json"
FORBIDDEN_CHANNEL_ID = 1518314179617095701

def load_levels():
    try:
        with open(LEVELS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_levels(levels):
    with open(LEVELS_FILE, 'w') as f:
        json.dump(levels, f, indent=4)

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
    await ctx.send(f"em progresso.")

@bot.command()
async def tigerai(ctx:commands.Context, *, query: str = ""):
    try:
        result = run_tiger_query(query)
        await ctx.send(f"```{result}```")
    except Exception as e:
        await ctx.send(f"Erro ao chamar tigerAi: {str(e)}")

@bot.command()
async def mommy(ctx:commands.Context):
    await ctx.send("https://media1.tenor.com/m/ibe09IFph04AAAAC/cool.gif")

@bot.command()
async def tiger(ctx:commands.Context):
    url: str = ("https://www.flamesofwar.com/Portals/0/all_images/Briefings/NorthAfrica/Tunisian-Tigers-01.jpg")
    await ctx.send(url)

@bot.command(name="erika")
async def erika(ctx: commands.Context):
    await ctx.send(
        "https://media.discordapp.net/attachments/1443943422246391919/1498066065153069146/IMG-20260421-WA0024.jpg?ex=69efce3e&is=69ee7cbe&hm=b293c846869edd0f7e959ab4f4239a51782dd18f6e1146"
    )

@bot.command(name="maho")
async def maho(ctx:  commands.Context):
    await ctx.send("https://media.discordapp.net/attachments/1443943422246391919/1498066065656250461/20260421_183600.jpg?ex=69efce3e&is=69ee7cbe&hm=6f71ab75860f2240ec531e4610bffe6faf2361ecefbae2b")

@bot.command()
async def jenzimibra(ctx:commands.Context):
    await ctx.send("https://preview.redd.it/jenzimibra-v0-3c59soouwfgd1.jpeg?width=640&crop=smart&auto=webp&s=298b84ac3810276df106d24b11bbca786353ea84")

@bot.command(name="ghost")
async def ghost(ctx:  commands.Context):
    await ctx.send("Vai tomar no cu, @mr.ghostzer0")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, motivo=None):
    await member.ban(reason=motivo)
    await ctx.send(f"{member} foi banido.")

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
async def isa(ctx:commands.Context):
    await ctx.send("https://i.pinimg.com/1200x/e3/c3/c7/e3c3c74130bbdf55da49f57fa0b8d34d.jpg")

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
async def lembrete(ctx, tempo: float, *, mensagem: str):
    await ctx.reply(f" Lembrete definido para {tempo}.")
    await asyncio.sleep(tempo * 60)
    await ctx.send(f"{ctx.author.mention}  {tempo} {mensagem}!")

@bot.command()
async def echo(ctx:commands.Context, *, mensagem: str):
    await ctx.send(mensagem)
    await ctx.message.delete()

@bot.command()
async def clear(ctx:commands.Context, quantidade: int):
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

@bot.command()
async def linkinpark(ctx:commands.Context):
    await ctx.send("https://www.youtube.com/watch?v=M9J6DKJXoKk")

@bot.command()
async def activity(ctx:commands.Context):
    await bot.change_presence(activity=discord.Game(name="War Thunder"))

@bot.event
async def on_member_join(member):
    boasvindas = bot.get_channel(1443943396581445692)
    mensagem = await boasvindas.send(
        f"Bem-vindo ao servidor, {member.mention}! Por favor, leia as regras. Todos a bordo do trem Hk! "
        "https://tenor.com/gT4pTVFK4Wj.gif"
    )
@bot.listen('on_message')
async def on_message_levels(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.TextChannel):
        # Obter o ID do usuário e do servidor
        user_id = str(message.author.id)
        guild_id = str(message.guild.id)

        levels = load_levels()

        if guild_id not in levels:
            levels[guild_id] = {}
        if user_id not in levels[guild_id]:
            levels[guild_id][user_id] = {"xp": 0, "level": 1}

        levels[guild_id][user_id]["xp"] += 10

        xp_needed = levels[guild_id][user_id]["level"] * 1000
        if levels[guild_id][user_id]["xp"] >= xp_needed:
            levels[guild_id][user_id]["level"] += 1
            await message.channel.send(
                f"Parabéns {message.author.mention}, você subiu para o nível {levels[guild_id][user_id]['level']}!"
            )

        save_levels(levels)

@bot.command()
async def ranking(ctx:commands.Context):
    guild_id = ctx.guild.id
    levels = load_levels()
    if str(guild_id) in levels:
        ranking = sorted(
            levels[str(guild_id)].items(),
            key=lambda x: (x[1]["level"], x[1]["xp"]),
            reverse=True,
        )
        ranking_message = "Ranking de Níveis:\n"
        for i, (user_id, data) in enumerate(ranking[:10], start=1):
            user = await bot.fetch_user(int(user_id))
            ranking_message += f"{i}. {user.name} - Nível {data['level']} (XP: {data['xp']})\n"
        await ctx.send(ranking_message)
    else:
        await ctx.send("Nenhum dado de níveis encontrado para este servidor.")

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
    limit = 1000
    messages = [message async for message in channel.history(limit=limit, oldest_first=True)]

    output = io.StringIO()
    for msg in messages:
        timestamp = msg.created_at.isoformat()
        author = msg.author
        content = msg.content
        output.write(f"[{timestamp}] {author}: {content}\n")

    output.seek(0)
    await ctx.send(file=discord.File(fp=output, filename=f"history_{channel.id}.txt"))

bot.run(os.getenv('DISCORD_TOKEN'))
