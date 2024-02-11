import nextcord
import re
import requests
import os
import yaml
import psutil
import cpuinfo
import loggerthyst as log
from .shared_data import SharedData
from nextcord.ext import commands


# LANG MAP FOR DISCORD EMBEDS
def update_language_map():
    linguist_url = "https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml"
    response = requests.get(linguist_url)
    if response.status_code != 200:
        log.error("Failed to fetch language mappings from GitHub")
    return yaml.safe_load(response.text)


def get_discord_syntax_highlighting(extension):
    language_map = update_language_map()
    discord_language_map = {}
    for language, properties in language_map.items():
        if "extensions" in properties:
            for ext in properties["extensions"]:
                discord_language_map[ext] = language.lower()
    return discord_language_map.get(extension, "")


# UTILS CLASS
class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # PING
    @nextcord.slash_command(
        description="Get the latency from the bot to Discords servers"
    )
    async def ping(self, interaction: nextcord.Interaction):
        latency = round(self.bot.latency * 1000, 0)
        embed = nextcord.Embed(title=f"Latency: {latency}MS", color=0x3346D1)
        await interaction.response.send_message(embed=embed)
        log.info(command="Ping", interaction=interaction)
        raise Exception("test")

    @nextcord.slash_command(description="Get information about the bot")
    async def info(self, interaction: nextcord.Interaction):

        cpu_info = cpuinfo.get_cpu_info()
        cpu_name = cpu_info["brand_raw"]
        python_version = cpu_info["python_version"]
        architecture = cpu_info["arch"]

        memory = psutil.virtual_memory()
        memory_used_gb = memory.used / (1024**3)
        memory_total_gb = memory.total / (1024**3)
        memory_percentage = memory.percent
        cpu = psutil.cpu_percent()

        shared_data = SharedData()
        bot_start_time = shared_data.get_bot_start_time()
        unix_timestamp = int(bot_start_time.timestamp())

        embed = nextcord.Embed(title="Info", color=0x3346D1)
        embed.add_field(
            name="Bot",
            value="Written in Python using the Nextcord wrapper for Discord.py and hosted on an OVH VPS\n[Source](https://github.com/Bluemethyst/Gitmethyst)",
        )
        embed.add_field(name="CPU", value=f"{cpu_name}\n{cpu.real}% in use")
        embed.add_field(name="Architecture", value=architecture)
        embed.add_field(
            name="Memory",
            value=f"{memory_used_gb:.2f}GB/{memory_total_gb:.2f}GB\n{memory_percentage}% in use",
        )
        embed.add_field(name="Python", value=python_version)
        embed.add_field(name="Startup Time", value=f"<t:{unix_timestamp}:R>")

        await interaction.response.send_message(embed=embed)
        log.info(command="Info", interaction=interaction)

    # GISTS AND GITHUB FILES PREVIEWER
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        await message.edit(suppress=True)

        github_pattern = (
            r"(https?://github\.com/[^/]+/[^/]+/blob(/[^/]+)*(/[^/]+)\.([^.]+))"
        )
        github_matches = re.findall(github_pattern, message.content)
        for url_tuple in github_matches:
            url = url_tuple[0]
            raw_url = url.replace("blob", "raw")
            _, file_extension = os.path.splitext(raw_url)
            discord_syntax = get_discord_syntax_highlighting(file_extension)

            response = requests.get(raw_url)

            if response.status_code == 200:
                file_content = f"```{discord_syntax}\n{response.text}"

                embed = nextcord.Embed(
                    title="File Content", description=file_content[:2042] + "...\n```"
                )
                embed.set_footer(text="Requested by " + str(message.author))

                await message.channel.send(embed=embed)
            else:
                log.error(f"Failed to fetch file content from {raw_url}")

        gist_pattern = r"(https?://gist\.github\.com/[^/]+/[^\s]+)"
        gist_matches = re.findall(gist_pattern, message.content)
        for url in gist_matches:

            gist_id = url.split("/")[-1]
            api_url = f"https://api.github.com/gists/{gist_id}"
            headers = {"Accept": "application/vnd.github+json"}
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                gist_data = response.json()
                file_name = list(gist_data["files"].keys())[0]
                file_extension = os.path.splitext(file_name)[1][1:]
                discord_syntax = get_discord_syntax_highlighting(file_extension)
                file_content = gist_data["files"][file_name]["content"]
                formatted_content = f"```{discord_syntax}\n{file_content}"
                embed = nextcord.Embed(
                    title="File Content",
                    description=formatted_content[:2042] + "...\n```",
                )
                embed.set_footer(text="Requested by " + str(message.author))

                await message.channel.send(embed=embed)
            else:
                log.error(f"Failed to fetch Gist content from {api_url}")
