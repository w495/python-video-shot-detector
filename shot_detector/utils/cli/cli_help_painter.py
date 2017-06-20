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
    usage=CliEscapeBrush(
        styles=[
            CliEscapeCodes.NORMAL
        ],
    ),
    prog=CliEscapeBrush(
        styles=[
            CliEscapeCodes.NORMAL
        ],
    ),
    text=CliEscapeBrush(),
    section=CliEscapeBrush(
        styles=[
            CliEscapeCodes.NORMAL,
        ],
    ),
    action_help=CliEscapeBrush(
        styles={
            CliEscapeCodes.RESET_ALL,
        },
    ),

    optional_short_name=CliEscapeBrush(
        styles={
            CliEscapeCodes.NORMAL,
        },
    ),

    optional_name=CliEscapeBrush(
        styles={
            CliEscapeCodes.BRIGHT,
        },
    ),

    optional_flag_name=CliEscapeBrush(
        styles={
            CliEscapeCodes.BRIGHT,
        },
    ),
    optional_flag_short_name=CliEscapeBrush(
        styles={
            CliEscapeCodes.BRIGHT,
        },
    ),

    optional_value_wrap=CliEscapeBrush(
        styles={
            CliEscapeCodes.DIM,
        },
    ),
    optional_value=CliEscapeBrush(
        styles={
            CliEscapeCodes.NORMAL,
            CliEscapeCodes.UNDERLINE,
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
            CliEscapeCodes.FG_CYAN,
        },
    ),
    metavar_default=CliEscapeBrush(
        styles={
            CliEscapeCodes.FG_RED,
        },
    ),
    default_name=CliEscapeBrush(
        styles={
            CliEscapeCodes.ITALIC,
            CliEscapeCodes.DIM,
        },
    ),
    default_value=CliEscapeBrush(
        styles={
            CliEscapeCodes.ITALIC,

        },
    ),



    literal=CliEscapeBrush(
        styles={
            CliEscapeCodes.FG_YELLOW,
        },
    ),

    interpreted=CliEscapeBrush(
        styles={
            CliEscapeCodes.FG_YELLOW,
        },
    ),

    emphasis=CliEscapeBrush(
        styles={
            CliEscapeCodes.ITALIC,
        },
    ),

    strong=CliEscapeBrush(
        styles={
            CliEscapeCodes.BRIGHT,
        },
    ),

    reference=CliEscapeBrush(
        styles={
            CliEscapeCodes.FG_BLUE,
        },
    ),

)
