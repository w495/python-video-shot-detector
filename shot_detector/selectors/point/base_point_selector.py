# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

from shot_detector.handlers import BaseEventHandler

from shot_detector.features.filters import AdaptiveThresholdFilter


from shot_detector.metrics import L1Norm

class BasePointSelector(BaseEventHandler):

    __logger = logging.getLogger(__name__)

    def select_point(self, event, video_state = None, *args, **kwargs):
        """
            Should be implemented
        """
        
        x, video_state = L1Norm.length(event.features, video_state)
        
        
        #video_state.x_event = False
        #if(x > 0.0):
        #video_state.x_event = True
        
        print (' [%s] %s:%s x = %s'%(event.time, 
                                video_state.frame_state.frame_number, 
                                video_state.packet_state.packet_number,
                                x))
    
        return event, video_state
