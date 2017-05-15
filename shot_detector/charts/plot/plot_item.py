# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from .plot_options import PlotOptions


class PlotItem(object):
    """
        ...
    """

    __slots__ = [
        'line_name',
        'axvline',
        'x_list',
        'y_list',
        'plot_options',
        'fmt',
        'plot_option_dict'

    ]

    def __init__(self,
                 line_name=None,
                 plot_options=None,
                 axvline=None,
                 x_list=None,
                 y_list=None,):
        """

        :param str line_name: 
        :param list of float x_list: 
        :param list of float y_list: 
        :param PlotOptions plot_options: 
        :param any axvline: 
        """

        self.line_name = line_name
        self.axvline = axvline

        self.x_list = x_list if x_list else list()
        self.y_list = y_list if y_list else list()

        self.plot_options = plot_options
        if not plot_options:
            self.plot_options = PlotOptions()

        self.fmt = self.plot_options.fmt

        label = self.plot_options.label
        if not label:
            label = line_name

        self.plot_option_dict = dict(
            label=label,
            linewidth=self.plot_options.width,
            linestyle=self.plot_options.style,
            color=self.plot_options.color,
            marker=self.plot_options.marker,
        )

    def update(self, x=None, y=None):
        """

        :param x: 
        :param y: 
        :return: 
        """
        self.x_list += [float(x)]
        self.y_list += [float(y)]
