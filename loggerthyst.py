import colorama
import nextcord
import os
from datetime import datetime
from colorama import Fore as f

colorama.init(autoreset=True)


def info(
    message: str = None, command: str = None, interaction: nextcord.Interaction = None
):
    """Logs as an info block with time and date to a file and prints to the console.
    \nUseful for logging certain events to make sure they happen as expected

    Args:
        message (str): The string you want to be logged as info
        command (str): The command you want info about
        interaction (nextcord.Interaction) The interaction you want info about
    """
    now = datetime.now()
    log_filename = f"{now.date()}.log"
    log_entry = ""
    if interaction and command:
        log_entry = (
            f"[INFO | {now.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"{command} used in {interaction.channel.id}, ({interaction.channel.name}) in guild {interaction.guild.id}, ({interaction.guild.name}) by user {interaction.user.id}, ({interaction.user.name})"
        )
    elif message:
        log_entry = f"[INFO | {now.strftime('%Y-%m-%d %H:%M:%S')}] " f"{message}"
    else:
        raise TypeError("Enter either message, or command and interaction")

    print(f.GREEN + log_entry)
    with open(log_filename, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry + "\n")


def warn(message: str):
    """Prints as a warning block with time and date.
    \nUseful for logging warnings on things that might not be ideal

    Args:
        message (str): The string you want to be printed as a warning
    """
    now = datetime.now()
    log_filename = f"{now.date()}.log"
    log_entry = f"[WARN | {now.strftime('%Y-%m-%d %H:%M:%S')}] " f"{message}"
    print(f.YELLOW + log_entry)
    with open(log_filename, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry + "\n")


def error(message: str):
    """Prints as an error block with time and date.
    \nUseful for logging errors such as features not working as expected

    Args:
        message (str): The string you want to be printed as an error
    """
    now = datetime.now()
    log_filename = f"{now.date()}.log"
    log_entry = f"[ERROR | {now.strftime('%Y-%m-%d %H:%M:%S')}] " f"{message}"
    print(f.YELLOW + log_entry)
    with open(log_filename, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry + "\n")


def fatal(message: str):
    """Prints as a fatal error block with time and date.
    \nUseful for logging fatal errors such as crashes

    Args:
        message (str): The string you want to be printed as a fatal error
    """
    now = datetime.now()
    log_filename = f"{now.date()}.log"
    log_entry = f"[FATAL | {now.strftime('%Y-%m-%d %H:%M:%S')}] " f"{message}"
    print(f.YELLOW + log_entry)
    with open(log_filename, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry + "\n")
