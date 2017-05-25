# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from functools import partial

from .cli_escape_brush import CliEscapeBrush, CliEscapeBrushString
from .cli_escape_codes import CliEscapeCodes
from .cli_escape_painter import CliEscapePainter

CliHelpPainterString = CliEscapeBrushString

cli_help_painter = CliEscapePainter(
    prog=CliEscapeBrush(
        styles=[
            CliEscapeCodes.FG_YELLOW,
            CliEscapeCodes.BRIGHT
        ],
    ),
    text=CliEscapeBrush(
        styles={
            CliEscapeCodes.FG_CYAN,
        },
    ),
    section=CliEscapeBrush(
        styles=[
            CliEscapeCodes.BRIGHT,
        ],
    ),
    action_help=partial(CliEscapeBrush.clean),
    optional_short_name=CliEscapeBrush(
        styles={
            CliEscapeCodes.FG_GREEN,
        },
    ),
    optional_name=CliEscapeBrush(
        styles={
            CliEscapeCodes.BRIGHT,
            CliEscapeCodes.FG_YELLOW,
            CliEscapeCodes.BG_YELLOW,
        },
    ),

    optional_flag_name=CliEscapeBrush(
        styles={
            CliEscapeCodes.BRIGHT,
            CliEscapeCodes.FG_GREEN,
        },
    ),
    optional_flag_short_name=CliEscapeBrush(
        styles={
            CliEscapeCodes.BRIGHT,
        },
    ),

    optional_value=CliEscapeBrush(
        styles={
            CliEscapeCodes.UNDERLINE,
        },
    ),
    optional_value_wrap=CliEscapeBrush(
        styles={
            CliEscapeCodes.FG_RED,
        },
    ),
    metavar_choices_wrap=CliEscapeBrush(
        styles={
            CliEscapeCodes.FG_MAGENTA,
        },
    ),
    metavar_choices=CliEscapeBrush(
        styles={
            CliEscapeCodes.FG_YELLOW,
        },
    ),
    metavar_action=CliEscapeBrush(
        styles={
            CliEscapeCodes.FG_GREEN,
        },
    ),
    metavar_default=CliEscapeBrush(
        styles={
            CliEscapeCodes.FG_GREEN,
        },
    ),
    default_name=CliEscapeBrush(
        styles={
            CliEscapeCodes.FG_GREEN,
        },
    ),
    default_value=CliEscapeBrush(
        styles={
            CliEscapeCodes.FG_CYAN,
        },
    ),
)
