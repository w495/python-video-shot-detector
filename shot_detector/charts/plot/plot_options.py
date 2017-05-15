# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function


from shot_detector.utils.tex_template import tex_template

class PlotOptions(object):
    """
        ...
    """

    __slots__ = [
        'fmt',
        'style',
        'label',
        'color',
        'width',
        'marker',
    ]

    def __init__(self,
                 *_,
                 label=None,
                 label_fmt=None,
                 fmt=None,
                 style=None,
                 color=None,
                 width=None,
                 marker=None):
        """
        
        :param str fmt: 
        :param str style: 
        :param str color: 
        :param float width: 
        :param str marker: 
        :param str label: 
        :param dict label_format: 
        """


        self.fmt = fmt
        if not self.fmt:
            self.fmt = str()
        self.style = style
        self.width = width
        self.color = color
        self.marker = marker

        self.label = label
        if label and label_fmt:
            self.label = tex_template(label, **label_fmt)

