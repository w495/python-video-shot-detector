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
from builtins import range

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


class RescalingVoteEventPlotter(BaseEventPlotter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    THRESHOLD = 0.8
    SLIDING_WINDOW_SIZE = 20

    NUMBER_OF_VOTERS = 16

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
        # noinspection PyUnusedLocal
        threshold = original > self.THRESHOLD
        #
        sad_filter = norm(l=1) | diff | abs
        sw = BaseSWFilter(
            size=self.SLIDING_WINDOW_SIZE,
            min_size=2
        )
        sw_max = sw | max
        sw_min = sw | min
        sw_norm = (original - sw_min) / (sw_max - sw_min)

        # sw_norm = NormSWFilter(min_size=2)

        sw_norm_seq = (sw_norm(size=25 * (i + 1)) for i in
                       range(self.NUMBER_OF_VOTERS))

        # noinspection PyUnusedLocal
        sw_vote_norm = sum(sw_norm_seq) / self.NUMBER_OF_VOTERS

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
                        size=400
                    )
                ),
                plot_options=PlotOptions(
                    style='-',
                    color='red',
                    width=1.0,
                ),
                formula=sad_filter | sw_norm(s=400)
            ),

            FilterDescription(
                name=(
                    '$D_{{\,{size},t}}'
                    '= sw\_norm_{{\,{size} }} D_{{t}}$'.format(
                        size=40
                    )
                ),
                plot_options=PlotOptions(
                    style='-',
                    color='orange',
                    width=1.0,
                ),
                formula=sad_filter | sw_norm(size=40)
            ),

            FilterDescription(
                name=(
                    '$D_{{\,{size},t}} '
                    '= sw\_norm_{{\,{size} }} D_{{t}}$'.format(
                        size=200
                    )
                ),
                plot_options=PlotOptions(
                    style='-',
                    color='orange',
                    width=1.0,
                ),
                formula=sad_filter | sw_norm(s=200)
            ),

            FilterDescription(
                name=(
                    '$D_{{\,{size},t}} '
                    '= sw\_norm_{{\,{size} }} D_{{t}}$'.format(
                        size=300
                    )
                ),
                plot_options=PlotOptions(
                    style='-',
                    color='violet',
                    width=1.0,
                ),
                formula=sad_filter | sw_norm(s=300)
            ),

            FilterDescription(
                # Sum of absolute difference filter.
                name='$D_{t} = ||F_{t} - F_{t-1}||_{L_1}$',
                plot_options=PlotOptions(
                    style='-',
                    color='blue',
                    width=2.0,
                ),
                formula=sad_filter
            ),

            FilterDescription(
                name=(
                    '$V_{v,t} = '
                    '\\frac{\sum^{i=v+1}_{i=1} '
                    'D_{\,{25 i},t}}{v}|_{v=16}$'
                ),
                plot_options=PlotOptions(
                    style='-',
                    color='green',
                    width=1.0,
                ),
                formula=sad_filter | sw_vote_norm
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
