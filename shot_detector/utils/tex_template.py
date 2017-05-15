# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from string import Template


def tex_template(template, **kwargs):
    """
    
    :param template: 
    :param kwargs: 
    :return: 
    """
    template = Template(template)
    string = template.substitute(**kwargs)
    return string
