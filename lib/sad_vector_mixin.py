# -*- coding: utf8 -*-

from __future__ import absolute_import

import numpy as np
import logging

from .base_vector_mixin import BaseVectorMixin

class SadVectorMixin(BaseVectorMixin):


    def handle_features(self, video_state, *args, **kwargs):
        '''
            FFMPEG-like method
            http://www.luckydinosaur.com/u/ffmpeg-scene-change-detector

        '''
        video_state = self.handle_curr_and_other(
            video_state.curr,
            video_state.prev,
            video_state,
            *args, **kwargs
        )

        return video_state

    def handle_curr_and_other(self, curr, other, video_state, *args, **kwargs):
        if (None != other.features):
            value = self.get_difference(curr.features, other.features)
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

    def get_difference(self, curr_features, other_features):
        '''
            FFMPEG-like method
            http://www.luckydinosaur.com/u/ffmpeg-scene-change-detector
        '''
        curr_vector =  np.array(curr_features)
        other_vector =  np.array(other_features)
        diff_vector = np.abs(curr_vector - other_vector)
        sad = np.sum(diff_vector)
        mean_sad = sad / (diff_vector.size * self.get_colour_size())
        return mean_sad
