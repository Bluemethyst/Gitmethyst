import nextcord
from nextcord.ext import commands
from github import Github
from github import Auth
import dotenv
import os
import requests
import github
import re
import loggerthyst as log


class GithubCommands(commands.Cog):
    def __init__(self, bot):
        dotenv.load_dotenv()
        self.bot = bot
        self.gh_token = Auth.Token(os.getenv("GITHUB_TOKEN"))
        self.g = Github(auth=self.gh_token)

    # REPO
    @nextcord.slash_command(description="View the information on a github repo")
    async def repo(
        self, interaction: nextcord.Interaction, username: str, repo_name: str
    ):
        await interaction.response.defer()
        try:
            repo = self.g.get_user(username).get_repo(repo_name)
            try:
                languages = repo.get_languages()
                most_used_language = max(languages, key=languages.get)
                response = requests.get(
                    "https://raw.githubusercontent.com/ozh/github-colors/master/colors.json"
                )
                language_colors = response.json()
                color_hex = language_colors.get(most_used_language, {}).get(
                    "color", "#FFFFFF"
                )
                final_color = int(color_hex.lstrip("#"), 16)
            except ValueError:
                final_color = 0xFFFFFF
            try:
                readme_content = (
                    repo.get_readme().decoded_content.decode("utf-8").strip()
                )

                readme_content = re.sub(r"\!\[[^\]]*\]\([^)]*\)", "", readme_content)

                if len(readme_content) > 2048:
                    readme_content = readme_content[:2048] + "..."
            except github.GithubException:
                readme_content = "No README found"

            embed = nextcord.Embed(
                url=f"https://github.com/{repo.owner.login}/{repo_name}",
                title=repo_name.capitalize(),
                color=final_color,
                description=readme_content,
            )
            embed.set_thumbnail(url=repo.owner.avatar_url)
            embed.add_field(
                name="<:git_star:1205317338203815956> Stars",
                value=repo.stargazers_count,
            )
            embed.add_field(
                name="<:git_fork:1205316317398433843> Forks", value=repo.forks_count
            )
            embed.add_field(
                name="<:git_issue:1205317336115052564> Open Issues",
                value=repo.open_issues_count,
            )
            await interaction.followup.send(embed=embed)
            log.info(
                f"Repo command used successfully in {interaction.guild.name}, {interaction.channel.name} by {interaction.user.name}"
            )
        except github.GithubException:
            await interaction.followup.send(
                "That repo does not exsit! If you believe this is a mistake please contact @Bluemethyst"
            )

    # ISSUES
    @nextcord.slash_command(description="Show issues on a repo")
    async def issues(
        self,
        interaction: nextcord.Interaction,
        username: str,
        repo_name: str,
        query: str = None,
    ):
        await interaction.response.defer()
        try:
            repo = self.g.get_user(username).get_repo(repo_name)
            try:
                languages = repo.get_languages()
                most_used_language = max(languages, key=languages.get)
                response = requests.get(
                    "https://raw.githubusercontent.com/ozh/github-colors/master/colors.json"
                )
                language_colors = response.json()
                color_hex = language_colors.get(most_used_language, {}).get(
                    "color", "#FFFFFF"
                )
                final_color = int(color_hex.lstrip("#"), 16)
            except ValueError:
                final_color = 0xFFFFFF
            try:
                if query:
                    search_results = self.g.search_issues(
                        query=f"repo:{username}/{repo_name} {query}"
                    )
                    issue_list = []
                    for issue in search_results:
                        issue_list.append(
                            f"[#{issue.number}: {issue.title}]({issue.html_url})"
                        )
                    issue_titles = "\n".join(issue_list)
                    if not issue_titles:
                        issue_titles = (
                            f"No issues found matching the search term '{query}'."
                        )
                    if len(issue_titles) > 2048:
                        issue_titles = issue_titles[:2048] + "..."
                else:
                    issues = repo.get_issues()
                    issue_list = []
                    for issue in issues:
                        issue_list.append(
                            f"[#{issue.number}: {issue.title}]({issue.html_url})"
                        )
                    issue_titles = "\n".join(issue_list)
                    if len(issue_titles) > 2048:
                        issue_titles = issue_titles[:2048] + "..."
            except github.GithubException:
                issue_titles = "An error occurred while fetching issues."
            if query:
                final_repo_name = f"{repo_name} Search Issue Results"
            else:
                final_repo_name = f"{repo_name} Active Issues"
            embed = nextcord.Embed(
                url=f"https://github.com/{repo.owner.login}/{repo_name}/issues",
                title=final_repo_name.capitalize(),
                color=final_color,
                description=issue_titles,
            )
            await interaction.followup.send(embed=embed)
            log.info(
                f"Issue command used successfully in {interaction.guild.name}, {interaction.channel.name} by {interaction.user.name}"
            )
        except github.GithubException:
            await interaction.followup.send("Repo doesnt seem to exsist")

    # PULLS
    @nextcord.slash_command(description="Show pull requests on a repo")
    async def pulls(
        self, interaction: nextcord.Interaction, username: str, repo_name: str
    ):
        await interaction.response.defer()
        try:
            repo = self.g.get_user(username).get_repo(repo_name)
            try:
                languages = repo.get_languages()
                most_used_language = max(languages, key=languages.get)
                response = requests.get(
                    "https://raw.githubusercontent.com/ozh/github-colors/master/colors.json"
                )
                language_colors = response.json()
                color_hex = language_colors.get(most_used_language, {}).get(
                    "color", "#FFFFFF"
                )
                final_color = int(color_hex.lstrip("#"), 16)
            except ValueError:
                final_color = 0xFFFFFF
            try:
                pulls = repo.get_pulls()
                pull_list = []
                for pull in pulls:
                    pull_list.append(f"[#{pull.number}: {pull.title}]({pull.html_url})")
                pull_titles = "\n".join(pull_list)
                if len(pull_titles) > 2048:
                    pull_titles = pull_titles[:2048] + "..."
            except github.GithubException:
                pull_titles = "No pulls found"

            embed = nextcord.Embed(
                url=f"https://github.com/{repo.owner.login}/{repo_name}/issues",
                title=repo_name.capitalize(),
                color=final_color,
                description=pull_titles,
            )
            await interaction.followup.send(embed=embed)
            log.info(
                f"Pulls command used successfully in {interaction.guild.name}, {interaction.channel.name} by {interaction.user.name}"
            )
        except github.GithubException:
            await interaction.followup.send("Repo doesnt seem to exsist")
