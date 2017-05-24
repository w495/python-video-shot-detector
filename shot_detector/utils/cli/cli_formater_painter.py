# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

import argparse
import re as _re
from functools import partial
from gettext import gettext as _

from .cli_brush import CliBrush
from .cli_codes import CliCodes

from .cli_painter import CliPainter, CliPainterString

cli_formatter_painter = CliPainter(
    prog=CliBrush(
        styles=[
            CliCodes.FG_YELLOW,
            CliCodes.BRIGHT
        ],
    ),
    text=CliBrush(
        styles={
            CliCodes.FG_CYAN,
        },
    ),
    section=CliBrush(
        styles=[
            CliCodes.BRIGHT,
        ],
    ),
    action_help=partial(CliBrush.clean),
    optional_short_name=CliBrush(
        styles={
            CliCodes.FG_GREEN,
        },
    ),
    optional_name=CliBrush(
        styles={
            CliCodes.BRIGHT,
            CliCodes.FG_YELLOW,
            CliCodes.BG_YELLOW,
        },
    ),

    optional_flag_name=CliBrush(
        styles={
            CliCodes.BRIGHT,
            CliCodes.FG_GREEN,
        },
    ),
    optional_flag_short_name=CliBrush(
        styles={
            CliCodes.BRIGHT,
        },
    ),

    optional_value=CliBrush(
        styles={
            CliCodes.UNDERLINE,
        },
    ),
    optional_value_wrap=CliBrush(
        styles={
            CliCodes.FG_RED,
        },
    ),
    metavar_choices_wrap=CliBrush(
        styles={
            CliCodes.FG_MAGENTA,
        },
    ),
    metavar_choices=CliBrush(
        styles={
            CliCodes.FG_YELLOW,
        },
    ),
    metavar_action=CliBrush(
        styles={
            CliCodes.FG_GREEN,
        },
    ),
    metavar_default=CliBrush(
        styles={
            CliCodes.FG_GREEN,
        },
    ),
    default_name=CliBrush(
        styles={
            CliCodes.FG_GREEN,
        },
    ),
    default_value=CliBrush(
        styles={
            CliCodes.FG_CYAN,
        },
    ),
)
