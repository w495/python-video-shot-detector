# -*- coding: utf8 -*-

from __future__ import absolute_import

from .base_vector_mixin import BaseVectorMixin

import numpy as np

class AdsVectorMixin(BaseVectorMixin):

    def handle_features(self, features, shot_state, thresold = 012, *args, **kwargs):
        '''
            absolute diff

        '''

        if (None != features.prev):
            curr = np.sum(features.curr)
            prev = np.sum(features.prev)
            diff = abs(curr - prev)
            mean = diff / (features.curr.size * 256)

            min_ = int(shot_state.times.curr / 60)
            sec_ = int(shot_state.times.curr % 60)

            if(thresold < mean):
                print 'x', min_, sec_,  shot_state.times.curr, mean, diff

        return shot_state
