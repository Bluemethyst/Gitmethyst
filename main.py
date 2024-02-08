from util.commands import Commands
from nextcord.ext import commands
import nextcord
import dotenv
import os

dotenv.load_dotenv()
bot = commands.Bot()
bot.add_cog(Commands(bot))

# https://github.com/PyGithub/PyGithub
# https://ghapi.fast.ai
# https://github.com/Bluemethyst/Gitmethyst

@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Game(name='your mother'))
    print(f"We have logged in as {bot.user}!")
    
bot.run(os.getenv("DISCORD_TOKEN"))