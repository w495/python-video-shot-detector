# -*- coding: utf8 -*-

from __future__ import absolute_import

import numpy as np
import logging

class ThresholdMixin(object):

    __logger = logging.getLogger(__name__)

    def handle_difference(self, value, video_state, thresold = 0.18):
        video_state.curr.value = value
        if(thresold < value):
            self.__logger.debug("%s sec = %s value = %s, thresold = %s"%(
                video_state.curr.time.time(),
                video_state.curr.time,
                value,
                thresold,
            ))
            video_state.cut_list += [video_state.curr]
            video_state.cut_counter += 1
        return video_state


