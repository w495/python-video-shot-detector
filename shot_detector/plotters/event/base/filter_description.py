# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from .plot_options import PlotOptions


class FilterDescription(object):

    def __init__(self,
                 name=None,
                 filter=None,
                 plot_options=None,
                 offset=None):
        """
        
        :param str name: 
        :param Filter filter: 
        :param PlotOptions plot_options: 
        :param float offset: 
        """

        self.name = name
        self.filter = filter


        self.plot_options = plot_options
        if not self.plot_options:
            self.plot_options = PlotOptions()

        self.offset = offset
        if not self.offset:
            self.offset = 0