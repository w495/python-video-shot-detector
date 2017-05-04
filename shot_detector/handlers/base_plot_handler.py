# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging
from collections import OrderedDict

import matplotlib
import matplotlib.pyplot as plt

from shot_detector.utils import common


class BasePlotHandler(object):
    """
        ...
    """
    __logger = logging.getLogger(__name__)
    __plot_buffer = OrderedDict()
    __line_list = []

    class PlotItem(object):
        """
            ...
        """

        def __init__(self,
                     x_list=None,
                     y_list=None,
                     style=None,
                     options=None):
            self.x_list = x_list
            if not self.x_list:
                self.x_list = list()
            self.y_list = y_list
            if not self.y_list:
                self.y_list = list()
            self.style = style
            if not self.style:
                self.style = str()
            self.options = options
            if not self.options:
                self.options = dict()

    def __init__(self, options=None):
        """
        
        :param options: 
        """
        self.kwargs = dict()
        if not options:
            options = dict()
        plot_xlabel = options.get('plot_xlabel', 't')
        plot_ylabel = options.get('plot_ylabel', 'L')
        plot_width = options.get('plot_width', 12.0)
        plot_height = options.get('plot_height', 9.0)
        plot_format = options.get('plot_format', 'pdf')
        plot_font_family = options.get(
            'plot_font_family',
            'DejaVu Sans'
        )
        plot_font_size = options.get('plot_font_size', 14)
        plot_save_dir = options.get('plot_save_dir', '.')

        self.xlabel = common.uni(plot_xlabel)
        self.ylabel = common.uni(plot_ylabel)

        # plt.rc('text', usetex=True)
        plt.rc('font', family=plot_font_family, size=plot_font_size)

        matplotlib.rcParams['figure.figsize'] = (
            plot_width, plot_height,
        )
        matplotlib.rcParams['savefig.format'] = plot_format
        matplotlib.rcParams['savefig.bbox'] = 'tight'
        matplotlib.rcParams['savefig.transparent'] = True
        matplotlib.rcParams['savefig.directory'] = plot_save_dir

    def add_data(self,
                 name,
                 key,
                 value,
                 plot_options=None,
                 **kwargs):
        """
        
        :param name: 
        :param key: 
        :param value: 
        :param plot_options: 
        :param kwargs: 
        :return: 
        """

        if not self.__plot_buffer.get(name):
            self.__plot_buffer[name] = BasePlotHandler.PlotItem()

        self.__plot_buffer[name].x_list += [key]
        self.__plot_buffer[name].y_list += [value]
        self.__plot_buffer[name].style = plot_options.expression
        self.__plot_buffer[name].options = dict(
            linewidth=plot_options.width,
            linestyle=plot_options.style,
            color=plot_options.color,
        )
        self.kwargs = kwargs

    def plot_data(self, name=None):
        """
        
        :param name: 
        :return: 
        """
        if name:
            self.plot_data_name(name)
        else:
            for name in self.__plot_buffer:
                self.plot_data_name(name)
        plt.legend(handles=self.__line_list)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        if self.kwargs.get('show_arrows'):
            self.show_arrows()

        plt.show()
        # plt.savefig('foo.pdf')

    def plot_data_name(self, name):
        """
        
        :param name: 
        :return: 
        """
        key_value = self.__plot_buffer.get(name)
        if key_value:
            if key_value.options.pop('axvline', False):
                for x in key_value.x_list:
                    plt.axvline(x, label=name, **key_value.options)
            else:
                line, = plt.plot(
                    key_value.x_list,
                    key_value.y_list,
                    key_value.style,
                    label=name,
                    **key_value.options
                )
                self.__line_list += [line]

    def show_arrows(self):
        """
        
        :return: 
        """
        fig = plt.gcf()
        ax = plt.gca()
        self.arrowed_spines(fig, ax)

    @staticmethod
    def arrowed_spines(fig, ax):
        """
        
        :param fig: 
        :param ax: 
        :return: 
        """

        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()

        # removing the default axis on all sides:
        # for side in ['bottom','right','top','left']:
        #     ax.spines[side].set_visible(False)

        # # removing the axis ticks
        # plt.xticks([]) # labels
        # plt.yticks([])
        # ax.xaxis.set_ticks_position('none') # tick markers
        # ax.yaxis.set_ticks_position('none')

        # get width and height of axes object to compute
        # matching arrowhead length and width
        dps = fig.dpi_scale_trans.inverted()
        bbox = ax.get_window_extent().transformed(dps)
        width, height = bbox.width, bbox.height

        # manual arrowhead width and length
        hw = 3. / 100. * (y_max - y_min)
        hl = 5. / 100. * (x_max - x_min)
        lw = 1.  # axis line width
        ohg = 0.3  # arrow overhang

        # compute matching arrowhead length and width
        yhw = hw / (y_max - y_min) * (x_max - x_min) * height / width
        yhl = hl / (x_max - x_min) * (y_max - y_min) * width / height

        # draw x and y axis
        ax.arrow(x_min, 0, x_max - x_min, 0., fc='k', ec='k', lw=lw,
                 head_width=hw, head_length=hl, overhang=ohg,
                 length_includes_head=True, clip_on=False)

        ax.arrow(0, y_min, 0., y_max - y_min, fc='k', ec='k', lw=lw,
                 head_width=yhw, head_length=yhl, overhang=ohg,
                 length_includes_head=True, clip_on=False)
