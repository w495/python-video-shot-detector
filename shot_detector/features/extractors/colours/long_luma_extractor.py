# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import

from ..base_extractor import BaseExtractor


# noinspection PyAbstractClass
class LongLumaExtractor(BaseExtractor):
    """
        ...
    """

    @staticmethod
    def av_format(**_):
        """
        
        :return: 
        """
        return 'gray16le'
