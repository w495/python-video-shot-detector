# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

import numpy as np


import matplotlib.pyplot as plt


from shot_detector.handlers import BaseEventHandler

from shot_detector.features.filters import AdaptiveThresholdFilter

from shot_detector.features.metrics import L1Norm, L2Norm


class PFilter(AdaptiveThresholdFilter):
    pass


class EFilter(AdaptiveThresholdFilter):
    pass



point_filter = PFilter()

event_filter = EFilter()

class BaseEventSelector(BaseEventHandler):

    __logger = logging.getLogger(__name__)

    point_data = []
    
    event_data = []
        
    def select_event(self, event, video_state = None, *args, **kwargs):
        """
            Should be implemented
        """
        
        point_flush_trigger = 'point_flush_trigger'
        event_flush_trigger = 'event_flush_trigger'
        
        
        
        features = event.features
        features, video_state = point_filter.filter_features(
            features = features, 
            video_state = video_state, 
            flush_trigger = point_flush_trigger,
            sigma_num = 3,
            window_size = 60,
            flush_limit = 60,
            window_limit = -1
        )
        point_diff, video_state = L2Norm.length(features, video_state)
        
        
        efeatures, video_state = L2Norm.length(event.features, video_state)
        
        self.point_data += [efeatures]
        
        print ('  [%s] %s:%s x = %s'%(event.time.time(), 
                                    video_state.frame_state.frame_number, 
                                    video_state.packet_state.packet_number,
                                    efeatures))
       
        
        
        #video_state.x_event = False
        ##if(x > 0.07):
        #video_state.x_event = True
        
        if (event.time > 1000):
            
            #x_val = [x[0] for x in self.point_data]
            #y_val = [x[1] for x in self.point_data]
            
            print

            plt.plot(self.point_data)
            plt.plot(self.event_data)
            
            plt.show()
            exit(1)

        
    
    
        return event, video_state
