from util.githubcmds import GithubCommands
from util.utils import Utils
from nextcord.ext import commands
import nextcord
import dotenv
import os
import datetime
import sys
import requests
import json
import loggerthyst as log
from util.shared_data import SharedData

intents = nextcord.Intents.all()
dotenv.load_dotenv()
bot = commands.Bot(intents=intents)
bot.add_cog(GithubCommands(bot))
bot.add_cog(Utils(bot))


# https://github.com/Bluemethyst/Gitmethyst


WEBHOOK_URL = os.getenv("DISCORD_ERROR_WEBHOOK")


async def send_exception_notification(extype, value, traceback, ctx):
    embed = {
        "title": "Unhandled Exception Occurred",
        "color": 0x3346D1,
        "fields": [
            {"name": "Type", "value": str(extype), "inline": False},
            {"name": "Context", "value": str(ctx), "inline": False},
            {"name": "Exception", "value": str(value), "inline": False},
            {"name": "Traceback", "value": str(traceback), "inline": False},
        ],
    }

    data = {
        "embeds": [embed],
        "username": "Gitmethyst",
        "avatar_url": "https://raw.githubusercontent.com/Bluemethyst/Gitmethyst/master/assets/gitmethyst.png",
    }

    result = requests.post(
        WEBHOOK_URL, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )

    if result.status_code != 204:
        print(
            f"Webhook failed with status code {result.status_code}. Response: {result.text}"
        )


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=nextcord.Activity(
            name="github requests", type=nextcord.ActivityType.listening
        )
    )
    shared_data = SharedData()
    shared_data.set_bot_start_time(datetime.datetime.now())
    log.info(f"We have logged in as {bot.user}!")


@bot.event
async def on_application_command_error(event, *args, **kwargs):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    await send_exception_notification(exc_type, exc_value, exc_traceback, args[0])


bot.run(os.getenv("DISCORD_TOKEN"))
