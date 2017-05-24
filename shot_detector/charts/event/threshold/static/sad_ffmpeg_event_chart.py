# -*- coding: utf8 -*-
"""
    The illustration different types of video-filters:
        * SadEventChart — sum of absolute difference filter
        * FfmpegLikeEventChart — FFMpeg-like shot detection filter.
    
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging

from shot_detector.utils.common import unique
from shot_detector.utils.log.log_meta import log_method_call_with
from .ffmpeg_like_event_chart import FfmpegLikeEventChart
from .sad_event_chart import SadEventChart


class SadFfmpegEventChart(SadEventChart, FfmpegLikeEventChart):
    """
        Chart for difference-based filters.
        
        It uses:
            * SadEventChart — sum of absolute difference filter;
            * FfmpegLikeEventChart — FFMpeg-like shot filter.
        
    """
    __logger = logging.getLogger(__name__)

    @log_method_call_with(logging.WARN)
    def seq_filters(self):
        """
            Chart options for Sad-filter and FFMpeg-kike illustration.
            
            :returns: filter chart options to describe filters.
            :rtype: list of FilterDescription
        """

        # Sum of absolute difference chat options.
        simple = SadEventChart.seq_filters(self)

        # FFMpeg-like shot detection chat options.
        ffmpeg_like = FfmpegLikeEventChart.seq_filters(self)

        # Deduplicate options union for each option set.
        result = unique(simple + ffmpeg_like)
        return result
