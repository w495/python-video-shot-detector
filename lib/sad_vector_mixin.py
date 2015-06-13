# -*- coding: utf8 -*-

from __future__ import absolute_import

from .base_vector_mixin import BaseVectorMixin

import numpy as np

class SadVectorMixin(BaseVectorMixin):


    def handle_features(self, features, shot_state, thresold = 0.12, *args, **kwargs):
        '''
            http://www.luckydinosaur.com/u/ffmpeg-scene-change-detector

        '''

        if (None != features.prev):
            difference = np.abs(features.curr - features.prev)
            sad = np.sum(difference)
            mafd = sad / (difference.size * self.get_colour_size())

            if(thresold < mafd):


                print 'y', shot_state.times.curr.time(),  shot_state.times.curr, mafd, sad
                shot_state.shot_counter

        return shot_state
