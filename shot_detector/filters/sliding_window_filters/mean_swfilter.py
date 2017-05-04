# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_swfilter import BaseStatSWFilter


class MeanSWFilter(BaseStatSWFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def aggregate_window_item(self, features, **kwargs):
        """
        
        :param features: 
        :param kwargs: 
        :return: 
        """
        features = self.try_ignore_last(features, **kwargs)
        return self.get_mean(features, **kwargs)

    @staticmethod
    def try_ignore_last(features, ignore_last=False, **_):
        """
        
        :param features: 
        :param ignore_last: 
        :param _: 
        :return: 
        """
        if ignore_last:
            features = list(features)[:-1]
        return features
