# -*- coding: utf8 -*-

from __future__ import absolute_import

import numpy as np
import logging



class BaseCompareMixin(object):

    def handle_features(self, video_state, *args, **kwargs):
        video_state = self.handle_curr_and_other(
            video_state.curr,
            video_state.prev,
            video_state,
            *args, **kwargs
        )
        return video_state

    def handle_curr_and_other(self, curr, other, video_state, *args, **kwargs):
        if (None != other.features):
            value, video_state = self.get_difference(
                curr.features,
                other.features,
                video_state,
                *args,
                **kwargs
            )
            video_state = self.handle_difference(
                value,
                video_state,
                *args,
                **kwargs
            )
        return video_state

    def handle_difference(self, value, video_state, *args, **kwargs):
        '''
            Should be implemented
        '''
        return video_state

    def get_difference(self, curr_features, other_features, video_state, *args, **kwargs):
        '''
            Should be implemented
        '''
        return None, video_state
