import nextcord
from nextcord.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @nextcord.slash_command(description="Get the latency from the bot to Discords servers")
    async def ping(self, interaction: nextcord.Interaction):
        latency = round(self.bot.latency * 1000, 0)
        await interaction.response.send_message(f"Bot Latency: {latency}MS")