# -*- coding: utf8 -*-

from __future__ import absolute_import

import numpy as np

from .base_compare_mixin import BaseCompareMixin

class BaseNorm(BaseCompareMixin):

    def calculate_distance(self, curr_features, other_features,
                           video_state, *args, **kwargs):
        '''
            calculate_distance
            Should be implemented
        '''
        return curr_features, video_state


    def get_item_size(self, image, video_state, *args, **kwargs):
        return 1, video_state

    def get_colour_size(self, image, video_state, *args, **kwargs):
        return 1, video_state
