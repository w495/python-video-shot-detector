# -*- coding: utf8 -*-

from __future__ import absolute_import

import numpy as np

from .base_compare_mixin import BaseCompareMixin

class SadMixin(BaseCompareMixin):

    def get_difference(self, curr_features, other_features):
        '''
            FFMPEG-like method
            http://www.luckydinosaur.com/u/ffmpeg-scene-change-detector
        '''
        curr_vector =  np.array(curr_features)
        other_vector =  np.array(other_features)
        diff_vector = np.abs(curr_vector - other_vector)
        sad = np.sum(diff_vector)
        mean_sad = 1.0 * sad  / (diff_vector.size * self.get_colour_size())
        return mean_sad

