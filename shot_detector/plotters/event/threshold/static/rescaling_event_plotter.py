# -*- coding: utf8 -*-

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging

from shot_detector.filters import (
    ShiftSWFilter,
    DelayFilter,
    NormFilter,
    BaseSWFilter,
)
from shot_detector.plotters.event.base_event_plotter import \
    BaseEventPlotter
from shot_detector.utils.log_meta import log_method_call_with


class RescalingEventPlotter(BaseEventPlotter):
    __logger = logging.getLogger(__name__)

    THRESHOLD = 0.8
    SLIDING_WINDOW_SIZE = 400

    @log_method_call_with(logging.WARN)
    def seq_filters(self):
        delay = DelayFilter()
        norm = NormFilter()
        shift = ShiftSWFilter()
        original = delay(0)
        diff = original - shift
        threshold = original > self.THRESHOLD

        sad_filter = diff | abs | norm(l=1)
        sw = BaseSWFilter(size=self.SLIDING_WINDOW_SIZE,
                          min_size=2)
        sw_max = sw | max
        sw_min = sw | min
        sw_norm = (original - sw_min) / (sw_max - sw_min)
        result_filter = sad_filter | sw_norm

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
                name='$D_{{\,{size},t}} '
                     '= sw\_norm_{{\,{size} }} D_{{t}}$'.format(
                    size=self.SLIDING_WINDOW_SIZE
                ),
                plot_options=dict(
                    linestyle='-',
                    color='green',
                    linewidth=1.0,
                ),
                filter=result_filter
            ),
            dict(
                name='$D_{t} = ||F_{t} - F_{t-1}||_{L_1}$',
                plot_options=dict(
                    linestyle='-',
                    color='blue',
                    linewidth=2.0,
                ),
                filter=sad_filter | norm(l=1)
            ),
            dict(
                # Sum of absolute differense filter > threshold.
                name='$D_{{\,{size},t}}  > T_{{const}} $'.format(
                    size=self.SLIDING_WINDOW_SIZE
                ),
                plot_options=dict(
                    linestyle=':',
                    color='teal',
                    linewidth=2.0,
                ),
                filter=result_filter | threshold
            ),
            dict(
                # The threshold value.
                name='$T_{{const}} = {} \in (0; 1)$'.format(
                    self.THRESHOLD),
                plot_options=dict(
                    linestyle='-',
                    color='black',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | self.THRESHOLD,
            ),
        )
