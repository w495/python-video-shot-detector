# -*- coding: utf8 -*-

from __future__ import absolute_import

import numpy as np

from base_compare_mixin import BaseCompareMixin

class AdsMixin(BaseCompareMixin):

    def get_difference(self, curr_features, other_features):
        '''
            FFMPEG-like method
            http://www.luckydinosaur.com/u/ffmpeg-scene-change-detector
        '''
        curr_vector =  np.array(curr_features)
        other_vector =  np.array(other_features)
        curr_sum = np.sum(curr_vector)
        prev_sum = np.sum(other_vector)
        diff_sum = abs(curr_sum - prev_sum)
        mean_diff = 1.0 * diff_sum  / (curr_vector.size * self.get_colour_size())
        return mean_sad
