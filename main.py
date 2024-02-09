from util.githubcmds import GithubCommands
from util.utils import Utils
from nextcord.ext import commands
import nextcord
import dotenv
import os
import loggerthyst as log

intents = nextcord.Intents.all()
dotenv.load_dotenv()
bot = commands.Bot(intents=intents)
bot.add_cog(GithubCommands(bot))
bot.add_cog(Utils(bot))

# https://github.com/PyGithub/PyGithub
# https://ghapi.fast.ai
# https://github.com/Bluemethyst/Gitmethyst


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=nextcord.Activity(
            name="github requests", type=nextcord.ActivityType.listening
        )
    )
    log.info(f"We have logged in as {bot.user}!")


bot.run(os.getenv("DISCORD_TOKEN"))
