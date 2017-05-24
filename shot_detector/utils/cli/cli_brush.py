# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

import os
import re
import sys

from shot_detector.utils.collections.obj_string import ObjString
from .cli_codes import CliCodes


class CliBrushString(ObjString):
    @staticmethod
    def clean(string):
        string = CliBrush.clean(string)
        return string

    def __len__(self):
        string = CliBrushString.clean(self)
        return len(string)


class CliBrush(object):
    def __init__(self, string=None, *_, styles=None):
        super(CliBrush, self).__init__()

        self._string = CliBrushString()
        if string:
            self._string = CliBrushString(string)

        self.always_color = False
        if os.environ.get('CLINT_FORCE_COLOR'):
            self.always_color = True

        self.styles = styles
        if not self.styles:
            self.styles = [CliCodes.RESET_ALL]

    @property
    def color_str(self):
        color_str = (
            '{start}'
            '{string}'
            '{stop}'.format(
                start=self.start,
                string=self._string,
                stop=self.stop,
            )
        )
        return color_str

    @property
    def start(self):
        color_str = ''.join(style.value for style in self.styles)
        return self.check_start_stop(color_str)

    @property
    def stop(self):
        color_str = '{reset_color}{reset_back}{reset_style}'.format(
            reset_color=CliCodes.FG_RESET.value,
            reset_back=CliCodes.BG_RESET.value,
            reset_style=CliCodes.RESET_ALL.value
        )
        return self.check_start_stop(color_str)

    def check_start_stop(self, color_str):
        if sys.stdout.isatty():
            return color_str
        else:
            return str()

    def __len__(self):
        string = CliBrush.clean(self._string)
        return len(string)

    def __repr__(self):
        return "<%s-string: '%s'>" % (self.color, self._string)

    def __str__(self):
        string = CliBrushString(self.color_str)
        string.obj = self
        return string

    def __iter__(self):
        return iter(self.color_str)

    def __add__(self, other):
        return CliBrushString(self.color_str + other)

    def __radd__(self, other):
        return CliBrushString(other + self.color_str)

    def __mul__(self, other):
        return (self.color_str * other)

    def __call__(self, string=None):
        return CliBrush(string=string, styles=self.styles)

    @staticmethod
    def clean(string='', **_):
        strip = re.compile(
            "([^-_a-zA-Z0-9!@#%&=,/'\";:~`\$\^\*\(\)\+\[\]\.\{\}\|\?\<\>\\]+|[^\s]+)")
        txt = strip.sub('', str(string))

        strip = re.compile(r'\[\d+m')
        txt = strip.sub('', txt)

        return txt
