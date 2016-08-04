# -*- coding: utf8 -*-

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging

from shot_detector.filters import (
    Filter,
    ShiftSWFilter,
    DelayFilter,
    NormFilter,
    # FFMpegLikeTresholdSWFilter
)
from shot_detector.plotters.event.base_event_plotter import \
    BaseEventPlotter
from shot_detector.utils.log_meta import log_method_call_with


class FfmpegLikeEventPlotter(BaseEventPlotter):
    __logger = logging.getLogger(__name__)

    THRESHOLD = 0.08

    @log_method_call_with(logging.INFO)
    def seq_filters(self):
        delay = DelayFilter()
        norm = NormFilter()
        shift = ShiftSWFilter()
        original = delay(0)
        diff = original - shift
        self.THRESHOLD = 0.08
        threshold = (original > self.THRESHOLD) * 1.1

        sad_filter = diff | abs | norm(l=1)

        sad_diff_filter = sad_filter | diff | abs

        ffmpeg_like = Filter.tuple(sad_filter, sad_diff_filter) | min

        # ffmpeg_like_hardcore = FFMpegLikeTresholdSWFilter()

        return (
            dict(
                # Original signal.
                name='$F_{L_1} = ||F_{t}||_{L_1}$',
                plot_options=dict(
                    linestyle='-',
                    color='gray',
                    linewidth=3.0,
                ),
                filter=norm(l=1),
            ),

            dict(
                name='$D^{ffmpeg}_{t} = \min(D_t, |D_t-D_{t-1}|)$',
                plot_options=dict(
                    linestyle='-',
                    color='red',
                    linewidth=2.0,
                ),
                filter=ffmpeg_like
            ),

            dict(
                name='$D^{ffmpeg}_{t} > T_{const} $',
                plot_options=dict(
                    linestyle=':',
                    color='orange',
                    linewidth=2.0,
                ),
                filter=ffmpeg_like | threshold
            ),
            dict(
                # The threshold value.
                name='$T_{{const}} = {threshold} \in (0; 1)$'.format(
                    threshold=self.THRESHOLD
                ),
                plot_options=dict(
                    linestyle='-',
                    color='black',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | self.THRESHOLD,
            ),
        )
