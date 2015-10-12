# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.utils.common import save_features_as_image

# from shot_detector.handlers import BasePointHandler



class BaseFilter(object):

    __logger = logging.getLogger(__name__)


    SUBFILTER_LIST = []


    def filter_features(self, features, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return features, video_state
 
    def filter_event_features(self, features, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return features, video_state
    
    def filter_point_features(self, features, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return features, video_state

    def filter_frame_features(self, features, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return features, video_state

    def get_subfilter_list(self, features, video_state, *args, **kwargs):
        """
            Should be implemented
        """        
        return kwargs.pop('subfilter_list', self.SUBFILTER_LIST)
    
    def apply_subfilters(self, features, video_state, filter_number = None, frame_number = None, *args, **kwargs):
        subfilter_list = self.get_subfilter_list(
            features,
            video_state,
            *args, **kwargs
        )

        for subfilter_number, (subfilter, options) in enumerate(subfilter_list):
            options.update(kwargs)
            features, video_state = subfilter.filter_features(
                features,
                video_state,
                **options
            )
            save_features_as_image(
                features=features,
                number=frame_number,
                subdir = "%s-%s-%s"%(
                    filter_number,
                    subfilter.__class__.__name__,
                    subfilter_number
                )
            )
        return features, video_state


