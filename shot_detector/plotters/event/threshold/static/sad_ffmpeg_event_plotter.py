# -*- coding: utf8 -*-

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging

from shot_detector.utils.common import unique
from shot_detector.utils.log_meta import log_method_call_with
from .ffmpeg_like_event_plotter import FfmpegLikeEventPlotter
from .sad_event_plotter import SadEventPlotter


class SadFfmpegEventPlotter(SadEventPlotter, FfmpegLikeEventPlotter):
    __logger = logging.getLogger(__name__)

    @log_method_call_with(logging.WARN)
    def seq_filters(self):
        """
        Returns the sequence of dict in which options of each chart
        are described.
        """
        simple = SadEventPlotter.seq_filters(self)
        ffmpeg_like = FfmpegLikeEventPlotter.seq_filters(self)
        result = unique(simple + ffmpeg_like)
        return result
