# -*- coding: utf8 -*-


"""
    Some utils
"""

from enum import Enum


class CliCodes(Enum):
    FG_BLACK = '\033[30m'
    FG_RED = '\033[31m'
    FG_GREEN = '\033[32m'
    FG_YELLOW = '\033[33m'
    FG_BLUE = '\033[34m'
    FG_MAGENTA = '\033[35m'
    FG_CYAN = '\033[36m'
    FG_WHITE = '\033[37m'
    FG_RESET = '\033[39m'
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_RESET = '\033[49m'

    BRIGHT = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'

    REV = '\033[7m'

    NORMAL = '\033[22m'
    RESET_ALL = '\033[0m'
