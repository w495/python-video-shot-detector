# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

from shot_detector.handlers import BaseEventHandler



from shot_detector.metrics import L1Norm

class BaseEventSelector(BaseEventHandler):

    __logger = logging.getLogger(__name__)

    def select_event(self, event, video_state = None, *args, **kwargs):
        """
            Should be implemented
        """
        
        x, video_state = L1Norm.length(event.features, video_state)
        
        
        if(x > 0):
            print (' [%s] %s:%s x = %s'%(event.time, 
                                    video_state.frame_state.frame_number, 
                                    video_state.packet_state.packet_number,
                                    x))
        
        return event, video_state
