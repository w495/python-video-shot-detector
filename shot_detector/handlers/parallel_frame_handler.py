# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from .base_frame_handler import BaseFrameHandler
from .parallel_base_handler import ParallelBaseHandler


def parallel_handle_image2(arg):
    """
    
    :param arg: 
    :return: 
    """
    self, features, frame, video_state = arg
    video_state = super(ParallelFameHandler,
                        self).handle_extracted_frame_features(
        features,
        frame,
        video_state,
    )
    return video_state


class ParallelFameHandler(BaseFrameHandler, ParallelBaseHandler):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def handle_extracted_frame_features(self, features, frame,
                                        video_state, process_pool=None,
                                        *args, **kwargs):
        """
        
        :param features: 
        :param frame: 
        :param video_state: 
        :param process_pool: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        if process_pool:
            process_pool.apply_async(
                func=self.handle_sequential_buffer,
                value=(features, frame),
                video_state=video_state,
                *args, **kwargs
            )

        return video_state

    @staticmethod
    def handle_sequential_buffer(**kwargs):
        """
        
        :param kwargs: 
        :return: 
        """
        # features, frame = features_frame
        video_state = kwargs.pop('video_state')
        prev_result = kwargs.pop('prev_result')
        if prev_result:
            video_state = prev_result
        # video_state = super(ParallelFameHandler, self)
        # .handle_extracted_frame_features(
        #         features,
        #         frame,
        # )
        return video_state
