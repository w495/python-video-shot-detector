# -*- coding: utf8 -*-

from __future__ import absolute_import

import math

import numpy as np

from .utils  import lucas_kanade


class OpticalFlow(object):

    def build_features(self, image, video_state = None, *args, **kwargs):
        if(None != video_state.curr.image):
            video_state.prev.image = video_state.curr.image
        else:
            video_state.prev.image = image
        video_state.curr.image = image
        flow = 1.0 * lucas_kanade(video_state.prev.image, video_state.curr.image)
        return flow, video_state


    def get_colour_size(self, image, video_state, *args, **kwargs):
        return 1, video_state

