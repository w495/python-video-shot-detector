# -*- coding: utf8 -*-

from __future__ import absolute_import

from .base_vector_mixin import BaseVectorMixin

import numpy as np

class SadVectorMixin(BaseVectorMixin):



    def handle_features(self, video_state, thresold = 0.12, *args, **kwargs):
        '''
            FFMPEG-like method
            http://www.luckydinosaur.com/u/ffmpeg-scene-change-detector

        '''

        if (None != video_state.prev.features):
            mafd = self.get_mafd(video_state.curr.features, video_state.prev.features)
            video_state.curr.value = mafd
            if(thresold < mafd):
                print 'y', video_state.curr.time.time(),  video_state.curr.time, mafd, sad
                video_state.cut_list += [video_state.curr]
                video_state.cut_counter += 1

        return video_state

    def get_mafd(self, curr, prev):
        difference = np.abs(video_state.curr.features - video_state.prev.features)
        sad = np.sum(difference)
        mafd = sad / (difference.size * self.get_colour_size())
        return mafd
