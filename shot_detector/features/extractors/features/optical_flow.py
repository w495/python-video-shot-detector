# -*- coding: utf8 -*-

from __future__ import absolute_import

from shot_detector.utils.numerical import lucas_kanade
from ..base_extractor import BaseExtractor


class OpticalFlow(BaseExtractor):
    """
        TODO: shoud be overwritten
    """
    
    def build_features(self, image, video_state=None, *args, **kwargs):
        if video_state.curr.image is not None:
            video_state.prev.image = video_state.curr.image
        else:
            video_state.prev.image = image
        video_state.curr.image = image
        flow = 1.0 * lucas_kanade(video_state.prev.image, video_state.curr.image)
        return flow, video_state

