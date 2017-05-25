# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from enum import Enum
from string import Template


class TemplateMode(Enum):
    """
        ...
    """
    TEXT = 'text'
    TEX = 'tex'


class TexTemplate(Template):
    """
        ...
    """

    template_mode = TemplateMode.TEXT

    def __init__(self, template, **kwargs):
        """
        
        :param template: 
        :param kwargs: 
        """

        if self.template_mode is TemplateMode.TEX:
            template = "${template}$".format(template=template)

        super(TexTemplate, self).__init__(template)
        self._string = self.safe_substitute(**kwargs)

    def __str__(self):
        return self._string


class TeX(TexTemplate):
    """
        ...
    """
    delimiter = '$$'


class Qtext(TexTemplate):
    """
        ...
    """
    delimiter = '?'
    template_mode = TemplateMode.TEXT


class Qtex(TexTemplate):
    """
        ...
    """
    delimiter = '?'
    template_mode = TemplateMode.TEX
