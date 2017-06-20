# -*- coding: utf8 -*-


"""
    Some utils
"""

import re

from enum import Enum


class CliEscapeCodes(Enum):
    """
        ...
    """

    # Foreground colours.

    FG_BLACK = '\u001b[30m'
    FG_RED = '\u001b[31m'
    FG_GREEN = '\u001b[32m'
    FG_YELLOW = '\u001b[33m'
    FG_BLUE = '\u001b[34m'
    FG_MAGENTA = '\u001b[35m'
    FG_CYAN = '\u001b[36m'
    FG_WHITE = '\u001b[37m'
    FG_RESET = '\u001b[39m'

    # Background colours.

    BG_BLACK = '\u001b[40m'
    BG_RED = '\u001b[41m'
    BG_GREEN = '\u001b[42m'
    BG_YELLOW = '\u001b[43m'
    BG_BLUE = '\u001b[44m'
    BG_MAGENTA = '\u001b[45m'
    BG_CYAN = '\u001b[46m'
    BG_WHITE = '\u001b[47m'
    BG_RESET = '\u001b[49m'

    # Styles.
    BRIGHT = '\u001b[1m'
    BOLD = '\u001b[1m'
    DIM = '\u001b[2m'
    ITALIC = '\u001b[3m'
    UNDERLINE = '\u001b[4m'
    REVERSED = '\u001b[7m'
    NORMAL = '\u001b[22m'
    RESET_ALL = '\u001b[0m'

    @classmethod
    def strip_seq(cls):
        """
        Prepare codes for regular expressions
        
        :return: 
        """
        for code in cls:
            strip = code.value
            strip = strip.replace('[', '\\[')
            yield strip

    @classmethod
    def strip_string(cls):
        """
        Concatenate prepared codes for regular expression
        
        :return: 
        """
        strip_seq = cls.strip_seq()
        strip_sting = '|'.join(strip_seq)
        strip_sting = "({})".format(strip_sting)
        return strip_sting

    @classmethod
    def strip_pattern(cls):
        """
        Compile re-pattern within prepared codes
        :return: 
        """
        strip_string = cls.strip_string()
        strip_pattern = re.compile(strip_string, re.U)
        return strip_pattern

    @classmethod
    def clean(cls, string=''):
        """
        Apply re.sub for pattern within prepared codes
        
        :param string: 
        :return: 
        """

        text = str(string)
        strip_pattern = cls.strip_pattern()
        text = strip_pattern.sub('', text)
        return text
