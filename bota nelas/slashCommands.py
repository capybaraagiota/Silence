import discord
from discord import app_commands
import random

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
        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ Este comando só pode ser usado em um servidor.",
                ephemeral=True,
            )
            return

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Você não tem permissão para sincronizar comandos.", ephemeral=True)
            return

        try:
            synced_commands = await bot.tree.sync()
            await interaction.response.send_message(
                f"✅ {len(synced_commands)} comandos sincronizados com sucesso!"
            )
        except discord.DiscordException as error:
            await interaction.response.send_message(
                f"❌ Erro ao sincronizar: {error}",
                ephemeral=True,
            )
