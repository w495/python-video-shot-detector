# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from .base_shot_detector import BaseShotDetector


class DummyTextDetector(BaseShotDetector):
    """
        ...
    """

    def detect(self, input_uri='', format_name=None, **kwargs):
        """
        
        :param input_uri: 
        :param format_name: 
        :param kwargs: 
        :return: 
        """
        pass
