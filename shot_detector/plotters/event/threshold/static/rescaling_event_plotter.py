# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

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
from shot_detector.plotters.event.base import (
    BaseEventPlotter,
    FilterDescription,
    PlotOptions
)
from shot_detector.utils.log_meta import log_method_call_with


class RescalingEventPlotter(BaseEventPlotter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    THRESHOLD = 0.8
    SLIDING_WINDOW_SIZE = 400

    @log_method_call_with(logging.WARN)
    def seq_filters(self):
        """
        
        :return: 
        """
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
            FilterDescription(
                # Original signal.
                name='$F_{L_1} = ||F_{t}||_{L_1}$',
                plot_options=PlotOptions(
                    style='-',
                    color='gray',
                    width=3.0,
                ),
                formula=norm(l=1),
            ),
            FilterDescription(
                name=(
                    '$D_{{\,{size},t}} '
                    '= sw\_norm_{{\,{size} }} D_{{t}}$'.format(
                        size=self.SLIDING_WINDOW_SIZE
                    )
                ),
                plot_options=PlotOptions(
                    style='-',
                    color='green',
                    width=1.0,
                ),
                formula=result_filter
            ),
            FilterDescription(
                name='$D_{t} = ||F_{t} - F_{t-1}||_{L_1}$',
                plot_options=PlotOptions(
                    style='-',
                    color='blue',
                    width=2.0,
                ),
                formula=sad_filter | norm(l=1)
            ),
            FilterDescription(
                # Sum of absolute difference filter > threshold.
                name=(
                    '$D_{{\,{size},t}}  > T_{{const}} $'.format(
                        size=self.SLIDING_WINDOW_SIZE
                    )
                ),
                plot_options=PlotOptions(
                    style=':',
                    color='teal',
                    width=2.0,
                ),
                formula=result_filter | threshold
            ),
            FilterDescription(
                # The threshold value.
                name=(
                    '$T_{{const}} = {} \in (0; 1)$'.format(
                        self.THRESHOLD
                    )
                ),
                plot_options=PlotOptions(
                    style='-',
                    color='black',
                    width=2.0,
                ),
                formula=norm(l=1) | self.THRESHOLD,
            ),
        )
