import datetime
import colorama
from colorama import Fore as f

colorama.init(autoreset=True)


def info(message: str):
    now = datetime.datetime.now()
    print(
        f.GREEN
        + f"[INFO | {now.strftime('%Y-%m-%d %H:%M:%S')}] "
        + f.WHITE
        + f"{message}"
    )


def warn(message: str):
    now = datetime.datetime.now()
    print(
        f.YELLOW
        + f"[INFO | {now.strftime('%Y-%m-%d %H:%M:%S')}] "
        + f.WHITE
        + f"{message}"
    )


def error(message: str):
    now = datetime.datetime.now()
    print(
        f.RED
        + f"[INFO | {now.strftime('%Y-%m-%d %H:%M:%S')}] "
        + f.WHITE
        + f"{message}"
    )


def fatal(message: str):
    now = datetime.datetime.now()
    print(
        f.LIGHTRED_EX
        + f"[INFO | {now.strftime('%Y-%m-%d %H:%M:%S')}] "
        + f.WHITE
        + f"{message}"
    )
