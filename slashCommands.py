import discord
from discord import app_commands
import random
import aiohttp
from discord import app_commands 

def register_slash_commands(bot):
    @bot.tree.command(name="oi", description="O bot te cumprimenta!")
    async def oi_slash(interaction: discord.Interaction):
        await interaction.response.send_message(f"Olá, {interaction.user.mention}!")

    @bot.tree.command(name="tiger", description="Envia a imagem da Tiger")
    async def tiger_slash(interaction: discord.Interaction):
        await interaction.response.send_message("https://www.flamesofwar.com/Portals/0/all_images/Briefings/NorthAfrica/Tunisian-Tigers-01.jpg")

    @bot.tree.command(name="gaymeter", description="Mede a porcentagem de gayzisse")
    async def gaymeter_slash(interaction: discord.Interaction):
        await interaction.response.send_message(f"O {interaction.user.mention} é {random.randint(0, 100)}% gay.")

    @bot.tree.command(name="pergunta", description="Faz uma pergunta de sim ou não")
    async def pergunta_slash(interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(['sim', 'não', 'talvez']))

    @bot.tree.command(name="sync", description="Sincroniza os comandos slash (Apenas Adm)")
    async def sync_slash(interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Sem permissão.", ephemeral=True)
            return
        await bot.tree.sync()
        await interaction.response.send_message("✅ Comandos sincronizados!")

    @bot.tree.command(name="help", description="Mostra os comandos disponíveis")
    async def help_slash(interaction: discord.Interaction):
        await interaction.response.send_message("Use .help para ver a lista completa de comandos de prefixo e / para os slash!")

    @bot.tree.command(name="sintonizar", description="Sintonize as frequências do New Empire")
    @app_commands.choices(radio=[
        app_commands.Choice(name="New Empire Rocks 🎸", value="rocks"),
        app_commands.Choice(name="New Empire Bangers 💥 (Em breve)", value="bangers"),
        app_commands.Choice(name="New Empire Blitz ⚡ (Em breve)", value="blitz"),
    ])
    async def sintonizar(interaction: discord.Interaction, radio: app_commands.Choice[str]):
        if radio.value == "rocks":
            await interaction.response.send_message(
                "**Sintonizando na frequência: New Empire Rocks...** 🎸\n"
                "`[||||||||||||||||||||] 100%`\n\n"
                "**Conectado!** Aumente o volume e prepare-se para a adrenalina.\n"
                "🔗 [Ouvir Agora](https://open.spotify.com/playlist/1pKl90hswFVzOmX2186vOZ?si=d0ed3e65f0804246)"
            )
        else:
            await interaction.response.send_message(
                f"**Sintonizando {radio.name}...**\n"
                "`[|||||               ] 25%`\n\n"
                "❌ **Sinal Fraco!** Esta frequência ainda está sendo calibrada pelo Alto Comando. Tente a *New Empire Rocks* enquanto isso!",
                ephemeral=True
            )