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


WEBHOOK_URL = "https://discord.com/api/webhooks/1206042036575277116/5xX_9E7HVfkcDOav0rXIh_2K7gXJ70DTouQP2XoWOOmqA06YZLOxW3PHRPZpRM_CpNM-"


async def send_exception_notification(exc, ctx):
    embed = {
        "title": "Unhandled Exception Occurred",
        "color": 0xFF0000,
        "fields": [
            {"name": "Context", "value": str(ctx), "inline": False},
            {"name": "Exception", "value": str(exc), "inline": False},
        ],
    }

    data = {
        "embeds": [embed],
        "username": "Your Bot Name",
        "avatar_url": "your_bot_avatar_url_here",
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
async def on_error(event, *args, **kwargs):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    await send_exception_notification(exc_value, args[0])


bot.run(os.getenv("DISCORD_TOKEN"))
