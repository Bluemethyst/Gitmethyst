import nextcord
from nextcord.ext import commands
from github import Github
from github import Auth
import dotenv
import os
import requests
import github
import re

class Commands(commands.Cog):
    def __init__(self, bot):
        dotenv.load_dotenv()
        self.bot = bot
        self.gh_token = Auth.Token(os.getenv('GITHUB_TOKEN'))
        self.g = Github(auth=self.gh_token)

        
    @nextcord.slash_command(description="Get the latency from the bot to Discords servers")
    async def ping(self, interaction: nextcord.Interaction):
        latency = round(self.bot.latency * 1000, 0)
        await interaction.response.send_message(f"Bot Latency: {latency}MS")
        
    @nextcord.slash_command(description=F"View the information to one of Bluemethysts github repos")
    async def repo(self, interaction: nextcord.Interaction, repo_name:str, username:str = None):
        await interaction.response.defer()
        try:
            if username == None:
                repo = self.g.get_user().get_repo(repo_name)
                try:
                    languages = repo.get_languages()
                    most_used_language = max(languages, key=languages.get)
                    response = requests.get('https://raw.githubusercontent.com/ozh/github-colors/master/colors.json')
                    language_colors = response.json()
                    color_hex = language_colors.get(most_used_language, {}).get('color', '#FFFFFF')
                    final_color = int(color_hex.lstrip('#'),  16)
                except ValueError:
                    final_color = 0xFFFFFF
                try:
                    readme_content = repo.get_readme().decoded_content.decode('utf-8').strip()

                    readme_content = re.sub(r'\!\[[^\]]*\]\([^)]*\)', '', readme_content)

                    if len(readme_content) >  2048:
                        readme_content = readme_content[:2048] + '...'
                except github.GithubException:
                    readme_content = "No README found"
                
                embed = nextcord.Embed(
                    url=f"https://github.com/{repo.owner.login}/{repo_name}",
                    title=f"{repo_name}", 
                    color=final_color,
                    description=readme_content)
                embed.set_thumbnail(url=repo.owner.avatar_url)
                embed.add_field(name="<:git_star:1205317338203815956>  Stars", value=repo.stargazers_count)
                embed.add_field(name="<:git_fork:1205316317398433843>  Forks", value=repo.forks_count)
                embed.add_field(name="<:git_issue:1205317336115052564>  Open Issues", value=repo.open_issues_count)
            else:
                repo = self.g.get_user(username).get_repo(repo_name)
                try:
                    languages = repo.get_languages()
                    most_used_language = max(languages, key=languages.get)
                    response = requests.get('https://raw.githubusercontent.com/ozh/github-colors/master/colors.json')
                    language_colors = response.json()
                    color_hex = language_colors.get(most_used_language, {}).get('color', '#FFFFFF')
                    final_color = int(color_hex.lstrip('#'),  16)
                except ValueError:
                    final_color = 0xFFFFFF
                try:
                    readme_content = repo.get_readme().decoded_content.decode('utf-8').strip()

                    readme_content = re.sub(r'\!\[[^\]]*\]\([^)]*\)', '', readme_content)

                    if len(readme_content) >  2048:
                        readme_content = readme_content[:2048] + '...'
                except github.GithubException:
                    readme_content = "No README found"
                
                embed = nextcord.Embed(
                    url=f"https://github.com/{repo.owner.login}/{repo_name}",
                    title=f"{repo_name}", 
                    color=final_color,
                    description=readme_content)
                embed.set_thumbnail(url=repo.owner.avatar_url)
                embed.add_field(name="<:git_star:1205317338203815956> Stars", value=repo.stargazers_count)
                embed.add_field(name="<:git_fork:1205316317398433843> Forks", value=repo.forks_count)
                embed.add_field(name="<:git_issue:1205317336115052564> Open Issues", value=repo.open_issues_count)
            await interaction.followup.send(embed=embed)
        except github.GithubException:
            await interaction.followup.send("That repo does not exsit! If you believe this is a mistake please contact @Bluemethyst")


        