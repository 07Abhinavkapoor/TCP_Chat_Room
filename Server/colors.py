RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
ORANGE = "\033[33m"
PURPLE = "\033[35m"
CYAN = "\033[36m"
PINK = "\033[95m"
LIGHTGREEN = "\033[92m"
LIGHTRED = "\033[91m"
LIGHTCYAN = "\033[96m"


def colorise(text, color):
    return color + text + RESET
