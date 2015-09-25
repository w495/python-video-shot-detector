# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.utils.multiprocessing import SaveStateProcessPool

from .base_frame_handler import BaseFrameHandler

from .parallel_base_handler import ParallelBaseHandler


class ParallelFameHandler(BaseFrameHandler, ParallelBaseHandler):

    __logger = logging.getLogger(__name__)


    def get_features(self, frame, video_state, *args, **kwargs):
        image, video_state = self.build_image(frame, video_state, *args, **kwargs)
        features, video_state = self.extract_features(image, video_state, *args, **kwargs)
        return features, video_state

    def handle_selected_frame(self, frame, video_state, process_pool=None, *args, **kwargs):
        if process_pool:
            process_pool.apply_async(
                func = self.handle_sequential_buffer,
                value = frame,
                video_state = video_state,
                *args, **kwargs
            )
        return video_state

    def handle_sequential_buffer(self, frame, video_state, prev_result=None, *args, **kwargs):
        if prev_result:
            video_state = prev_result
        video_state = super(ParallelFameHandler, self).handle_selected_frame(
            frame,
            video_state,
            *args, **kwargs
        )
        return video_state
