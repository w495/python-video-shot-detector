# -*- coding: utf8 -*-

from __future__ import absolute_import

import numpy as np

from base_compare_mixin import BaseCompareMixin

class AdsMixin(BaseCompareMixin):

    def get_difference(self, curr_features, other_features, video_state, *args, **kwargs):
        '''
            FFMPEG-like method
            http://www.luckydinosaur.com/u/ffmpeg-scene-change-detector
        '''
        curr_vector =  np.array(curr_features)
        other_vector =  np.array(other_features)
        curr_sum = np.sum(curr_vector)
        prev_sum = np.sum(other_vector)
        diff_sum = abs(curr_sum - prev_sum)
        colour_size, video_state = self.get_colour_size(
            curr_vector,
            video_state,
            *args,
            **kwargs
        )
        mean_diff = 1.0 * diff_sum  / (curr_vector.size * colour_size)
        return mean_diff, video_state
