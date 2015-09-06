# -*- coding: utf8 -*-

from __future__ import absolute_import

class BaseSelector(object):

    def select_transition(self, video_state, *args, **kwargs):
        video_state = self.select_pair(
            video_state.curr,
            video_state.prev,
            video_state,
            *args, **kwargs
        )
        return video_state

    def select_pair(self, curr, other, video_state, *args, **kwargs):
        if (None != other.features):
            value, video_state = self.calculate_distance(
                curr.features,
                other.features,
                video_state,
                *args,
                **kwargs
            )
            video_state = self.select_distance(
                value,
                video_state,
                *args,
                **kwargs
            )
        return video_state

    def select_distance(self, value, video_state, *args, **kwargs):
        '''
            Should be implemented
        '''
        return video_state

    def calculate_distance(self, curr_features, other_features,
                           video_state, *args, **kwargs):
        '''
            calculate_distance
            Should be implemented
        '''
        return curr_features, video_state
