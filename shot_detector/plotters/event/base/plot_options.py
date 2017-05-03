# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function



class PlotOptions(object):

    def __init__(self,
                 expression=None,
                 style=None,
                 color=None,
                 width=None,
                 marker=None):
        """
        
        :param str expression: 
        :param str style: 
        :param str color: 
        :param float width: 
        """
        self.expression = expression
        if not self.expression:
            self.expression = str()
        self.style = style
        self.width = width
        self.color = color
        self.marker = marker
