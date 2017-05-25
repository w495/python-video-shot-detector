# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

import os
import sys

from shot_detector.utils.collections.obj_string import ObjString
from .cli_escape_codes import CliEscapeCodes


class CliEscapeBrushString(ObjString):
    """
        ...
    """

    @staticmethod
    def clean(string):
        """
        
        :param string: 
        :return: 
        """
        string = CliEscapeBrush.clean(string)
        return string

    def __len__(self):
        """
        
        :return: 
        """
        string = CliEscapeBrushString.clean(self)
        return len(string)


class CliEscapeBrush(object):
    """
        ...
    """

    def __init__(self, string=None, *_, styles=None):
        """
        
        :param string: 
        :param _: 
        :param styles: 
        """
        super(CliEscapeBrush, self).__init__()

        self._string = CliEscapeBrushString()
        if string:
            self._string = CliEscapeBrushString(string)

        self.always_color = False
        if os.environ.get('CLINT_FORCE_COLOR'):
            self.always_color = True

        self.styles = styles
        if not self.styles:
            self.styles = [CliEscapeCodes.RESET_ALL]

    @property
    def color_str(self):
        """
        
        :return: 
        """
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
        """
        
        :return: 
        """
        color_str = ''.join(style.value for style in self.styles)
        return self.check_start_stop(color_str)

    @property
    def stop(self):
        """
        
        :return: 
        """
        color_str = '{reset_color}{reset_back}{reset_style}'.format(
            reset_color=CliEscapeCodes.FG_RESET.value,
            reset_back=CliEscapeCodes.BG_RESET.value,
            reset_style=CliEscapeCodes.RESET_ALL.value
        )
        return self.check_start_stop(color_str)

    @staticmethod
    def check_start_stop(color_str):
        """
        
        :param color_str: 
        :return: 
        """
        if sys.stdout.isatty():
            return color_str
        else:
            return str()

    def __len__(self):
        """
        
        :return: 
        """
        string = CliEscapeBrush.clean(self._string)
        return len(string)

    def __repr__(self):
        """
        
        :return: 
        """
        return "<%s-string: '%s'>" % (self.color, self._string)

    def __str__(self):
        """
        
        :return: 
        """
        string = CliEscapeBrushString(self.color_str)
        string.obj = self
        return string

    def __iter__(self):
        """
        
        :return: 
        """
        return iter(self.color_str)

    def __add__(self, other):
        """
        
        :param other: 
        :return: 
        """
        return CliEscapeBrushString(self.color_str + other)

    def __radd__(self, other):
        """
        
        :param other: 
        :return: 
        """
        return CliEscapeBrushString(other + self.color_str)

    def __mul__(self, other):
        """
        
        :param other: 
        :return: 
        """
        return CliEscapeBrushString(self.color_str * other)

    def __call__(self, string=None):
        """
        
        :param string: 
        :return: 
        """
        return CliEscapeBrush(string=string, styles=self.styles)

    @staticmethod
    def clean(string='', **_):
        """
        
        :param string: 
        :param _: 
        :return: 
        """

        text = CliEscapeCodes.clean(string)
        return text
