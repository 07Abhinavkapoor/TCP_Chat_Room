RESET = "\033[0m"
RED = "\033[31m"
colors = [
    "\033[93m",  # YELLOW
    "\033[36m",  # CYAN
    "\033[95m",  # PINK
    "\033[34m"  # BLUE
]


def colorise(text, index):
    return colors[index] + text + RESET
