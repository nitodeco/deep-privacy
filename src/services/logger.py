from colorama import Fore, Style


def info(message: str):
    print(f"{Fore.GREEN}[INFO] {Style.RESET_ALL}{message}")


def warn(message: str):
    print(f"{Fore.YELLOW}[WARNING] {Style.RESET_ALL}{message}")


def debug(message: str):
    print(f"{Fore.BLUE}[DEBUG] {Style.RESET_ALL}{message}")


def error(message: str):
    print(f"{Fore.RED}[ERROR] {Style.RESET_ALL}{message}")
