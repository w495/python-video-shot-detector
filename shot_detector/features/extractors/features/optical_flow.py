# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import

from shot_detector.utils.numerical import lucas_kanade
from ..base_extractor import BaseExtractor


# noinspection PyAbstractClass
class OpticalFlow(BaseExtractor):
    """
        TODO: should be overwritten
    """

    # noinspection PyUnusedLocal
    @staticmethod
    def build_features(image, video_state=None, **_kwargs):
        """
        
        :param image: 
        :param video_state: 
        :param _kwargs: 
        :return: 
        """
        if video_state.curr.image is not None:
            video_state.prev.image = video_state.curr.image
        else:
            video_state.prev.image = image
        video_state.curr.image = image
        flow = 1.0 * lucas_kanade(video_state.prev.image,
                                  video_state.curr.image)
        return flow, video_state
