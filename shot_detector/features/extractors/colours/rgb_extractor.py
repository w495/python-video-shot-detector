# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from ..base_extractor import BaseExtractor


# noinspection PyAbstractClass
class RgbExtractor(BaseExtractor):
    """
        ...
    """

    # noinspection PyUnusedLocal
    @staticmethod
    def av_format(**_kwargs):
        """
        
        :param _kwargs: 
        :return: 
        """
        return 'rgb24'
