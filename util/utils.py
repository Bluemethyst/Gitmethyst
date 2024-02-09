import nextcord
import re
import requests
import os
import yaml
import loggerthyst as log
from nextcord.ext import commands


# LANG MAP FOR DISCORD EMBEDS
def update_language_map():
    linguist_url = "https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml"
    response = requests.get(linguist_url)
    if response.status_code != 200:
        raise Exception("Failed to fetch language mappings from GitHub Linguist")
    return yaml.safe_load(response.text)


def get_discord_syntax_highlighting(extension):
    language_map = update_language_map()
    discord_language_map = {}
    for language, properties in language_map.items():
        if "extensions" in properties:
            for ext in properties["extensions"]:
                discord_language_map[ext] = language.lower()
    return discord_language_map.get(extension, "")


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        description="Get the latency from the bot to Discords servers"
    )
    async def ping(self, interaction: nextcord.Interaction):
        latency = round(self.bot.latency * 1000, 0)
        await interaction.response.send_message(f"Bot Latency: {latency}MS")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        github_pattern = (
            r"(https?://github\.com/[^/]+/[^/]+/blob(/[^/]+)*(/[^/]+)\.([^.]+))"
        )
        matches = re.findall(github_pattern, message.content)
        for url_tuple in matches:
            url = url_tuple[0]
            raw_url = url.replace("blob", "raw")
            _, file_extension = os.path.splitext(raw_url)
            discord_syntax = get_discord_syntax_highlighting(file_extension)

            response = requests.get(raw_url)

            if response.status_code == 200:
                file_content = f"```{discord_syntax}\n{response.text}"

                embed = nextcord.Embed(
                    title="File Content", description=file_content[:2045] + "```"
                )
                embed.set_footer(text="Requested by " + str(message.author))

                await message.channel.send(embed=embed)
            else:
                log.error(f"Failed to fetch file content from {raw_url}")
