# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging
import os
from collections import Mapping
from collections import OrderedDict
from enum import Enum

import matplotlib
import matplotlib.pyplot as plt
import six
from past.builtins import unicode

from shot_detector.utils import NotNoneKwDefaultsObject
from .plot_item import PlotItem
from .plot_options import PlotOptions


class PlotMode(Enum):
    """
        ...
    """
    SHOW_PLOT = 'show-plot'
    SAVE_PLOT = 'save-plot'


class ArrowsVariant(Enum):
    """
        ...
    """
    TRIANGLE = 'with arrows'
    NONE = None


class Plotter(NotNoneKwDefaultsObject):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    plot_buffer = OrderedDict()

    Mode = PlotMode

    ArrowsVariant = ArrowsVariant

    def __init__(self, *_,
                 xlabel='t',
                 ylabel='L',
                 width=12.0,
                 height=9.0,
                 font_family='DejaVu Sans',
                 font_size=14,
                 save_format='pdf',
                 save_name='plot.pdf',
                 save_dir='.',
                 display_mode=None,
                 arrows_mode=None):
        """
        
        :param str xlabel: 
        :param str ylabel: 
        :param float width: 
        :param float height: 
        :param str font_family: 
        :param int font_size: 
        :param str save_format: 
        :param str save_name: 
        :param str save_dir: 
        :param set of PlotMode display_mode: 
        :param ArrowsVariant arrows_mode: 
        """
        self.init_dict = self.option_dict(local_dict=locals())

        self.save_name = save_name
        self.save_dir = save_dir
        self.display_mode = display_mode
        if not display_mode:
            self.display_mode = set()

        self.arrows_mode = arrows_mode
        self.xlabel = unicode(xlabel)
        self.ylabel = unicode(ylabel)

        self.width = width
        self.height = height
        self.font_family = font_family
        self.font_size = font_size
        self.save_format = save_format
        self.save_dir = save_dir

        self.rc_configure()

    def __call__(self, **kwargs):
        self_type = type(self)
        options = dict(
            self.init_dict,
            **kwargs
        )
        return self_type(**options)

    def option_dict(self, local_dict):
        """
        
        :param local_dict: 
        :return: 
        """
        local_seq = self.option_seq(local_dict)
        return dict(local_seq)

    @staticmethod
    def option_seq(local_dict):
        """
        
        :param local_dict: 
        :return: 
        """
        local_items = six.iteritems(local_dict)
        bad_locals = {'_', 'self'}
        for key, value in local_items:
            if key not in bad_locals:
                yield key, value

    def rc_configure(self):
        """
        
        :return: 
        """
        self._rc_configure(
            width=self.width,
            height=self.height,
            font_family=self.font_family,
            font_size=self.font_size,
            save_format=self.save_format,
            save_dir=self.save_dir,
        )

    @staticmethod
    def _rc_configure(width=12.0,
                      height=9.0,
                      font_family='DejaVu Sans',
                      font_size=14,
                      save_format='pdf',
                      save_dir='.'):
        """
        
        :param float width: 
        :param float height: 
        :param str font_family: 
        :param int font_size: 
        :param str save_format: 
        :param str save_dir: 
        :return: 
        """

        # plt.rc('text', usetex=True)
        plt.rc('font', family=font_family, size=font_size)

        matplotlib.rcParams['figure.figsize'] = (
            width, height,
        )
        matplotlib.rcParams['savefig.format'] = save_format
        matplotlib.rcParams['savefig.bbox'] = 'tight'
        matplotlib.rcParams['savefig.transparent'] = True
        matplotlib.rcParams['savefig.directory'] = save_dir

    def add_point(self,
                  line_name,
                  key,
                  value,
                  plot_options=None):
        """
        
        :param str line_name: 
        :param float key: 
        :param float value: 
        :param PlotOptions plot_options: 
        :return: 
        """

        item = self.plot_buffer.get(line_name)

        if not item:
            item = PlotItem(
                line_name=line_name,
                plot_options=plot_options,
            )
            self.plot_buffer[line_name] = item

        item.update(x=key, y=value)

    def reveal(self,
               line_name=None,
               display_mode=None,
               arrows_mode=None,
               save_name=None):
        """
        
        :param str line_name: 
        :param PlotMode display_mode: 
        :param ArrowsVariant arrows_mode: 
        :param str save_name: 
        :return: 
        """

        self.plot_chart(line_name=line_name)
        self.may_plot_arrows(arrows_mode=arrows_mode)
        self.display(
            display_mode=display_mode,
            save_name=save_name,
        )

    def plot_chart(self, line_name=None):
        """
        
        :param str line_name: 
        :return: 
        """

        line_list = self.plot_lines(line_name=line_name)
        self.plot_legend(line_list)

    def may_plot_arrows(self, arrows_mode=None):
        """
        
        :param ArrowsVariant arrows_mode: 
        :return: 
        """

        if arrows_mode is None:
            arrows_mode = self.arrows_mode
        if arrows_mode is ArrowsVariant.TRIANGLE:
            self.plot_arrows()

    def display(self, display_mode=None, save_name=None):
        """
        
        :param PlotMode display_mode: 
        :param str  save_name: 
        :return: 
        """

        if display_mode is None:
            display_mode = self.display_mode

        if PlotMode.SAVE_PLOT in display_mode:
            self.may_save_figure(save_name=save_name)
        if PlotMode.SHOW_PLOT in display_mode:
            self.may_show_figure()

    def may_save_figure(self, save_name=None):
        """
        
        :param str save_name: 
        :return: 
        """
        if save_name is None:
            save_name = self.save_name

        dir_name = os.path.dirname(save_name)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        plt.savefig(save_name)

    def may_show_figure(self):
        """
        
        :return: 
        """
        dir_name = self.save_dir
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        plt.show()

    def plot_lines(self, line_name):
        """
        
        :param line_name: 
        :return: 
        """
        if line_name:
            return self.plot_line(line_name)
        return self.plot_line_from_buffer()

    def plot_line_from_buffer(self):
        """
        
        :return: 
        """
        seq = self.plot_line_from_buffer_seq()
        return list(seq)

    def plot_line_from_buffer_seq(self):
        """
        
        :return: 
        """
        for line_name, item in six.iteritems(self.plot_buffer):
            line_seq = self.plot_line_seq(item=item)
            for line in line_seq:
                yield line

    def plot_legend(self, line_list=None):
        """
        
        :param list line_list: 
        :return: 
        """
        plt.legend(handles=line_list)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

    def plot_line(self, line_name):
        """
        
        :param str line_name: 
        :return: 
        """
        item = self.plot_buffer.get(line_name)
        line_seq = self.plot_line_seq(item=item)
        return list(line_seq)

    def plot_line_seq(self, item=None):
        """
        
        :param PlotItem item: 
        :return: 
        """

        if item.axvline:
            self.plot_axv_line(item=item)
        else:
            line = self.plot_simple_line(item=item)
            yield line

    def plot_axv_line(self, item=None):
        """
         
        :param PlotItem item: 
        :return: 
        """
        axvline_seq = self.plot_axv_line_seq(item=item)
        axvline_list = list(axvline_seq)
        return axvline_list

    @staticmethod
    def plot_axv_line_seq(item=None):
        """
        
        :param PlotItem item: 
        :param item: 
        :return: 
        """
        for x in item.x_list:
            yield plt.axvline(x, **item.plot_option_dict)

    @staticmethod
    def plot_simple_line(item=None):
        """
        
        :param PlotItem item: 
        :return: 
        """

        line, = plt.plot(
            item.x_list,
            item.y_list,
            item.fmt,
            **item.plot_option_dict
        )
        return line

    def plot_arrows(self):
        """
        
        :return: 
        """
        fig = plt.gcf()
        ax = plt.gca()
        self.plot_arrowed_spines(fig, ax)

    @staticmethod
    def plot_arrowed_spines(fig, ax):
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
