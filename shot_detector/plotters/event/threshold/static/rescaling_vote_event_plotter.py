# -*- coding: utf8 -*-

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging

# PY2 & PY3 — compatibility
from builtins import range

from shot_detector.filters import (
    ShiftSWFilter,
    DelayFilter,
    NormFilter,
    BaseSWFilter,
)
from shot_detector.plotters.event.base_event_plotter import \
    BaseEventPlotter
from shot_detector.utils.log_meta import log_method_call_with


class RescalingVoteEventPlotter(BaseEventPlotter):
    __logger = logging.getLogger(__name__)

    THRESHOLD = 0.8
    SLIDING_WINDOW_SIZE = 20

    NUMBER_OF_VOTERS = 16

    @log_method_call_with(logging.WARN)
    def seq_filters(self):
        delay = DelayFilter()
        norm = NormFilter()
        shift = ShiftSWFilter()
        original = delay(0)
        diff = original - shift
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

        sw_vote_norm = sum(sw_norm_seq) / self.NUMBER_OF_VOTERS

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
                    size=400
                ),
                plot_options=dict(
                    linestyle='-',
                    color='red',
                    linewidth=1.0,
                ),
                filter=sad_filter | sw_norm(s=400)
            ),

            dict(
                name='$D_{{\,{size},t}} 1'
                     '= sw\_norm_{{\,{size} }} D_{{t}}$'.format(
                    size=40
                ),
                plot_options=dict(
                    linestyle='-',
                    color='orange',
                    linewidth=1.0,
                ),
                filter=sad_filter | sw_norm(size=40)
            ),

            dict(
                name='$D_{{\,{size},t}} '
                     '= sw\_norm_{{\,{size} }} D_{{t}}$'.format(
                    size=200
                ),
                plot_options=dict(
                    linestyle='-',
                    color='orange',
                    linewidth=1.0,
                ),
                filter=sad_filter | sw_norm(s=200)
            ),

            dict(
                name='$D_{{\,{size},t}} '
                     '= sw\_norm_{{\,{size} }} D_{{t}}$'.format(
                    size=300
                ),
                plot_options=dict(
                    linestyle='-',
                    color='violet',
                    linewidth=1.0,
                ),
                filter=sad_filter | sw_norm(s=300)
            ),

            dict(
                # Sum of absolute differense filter.
                name='$D_{t} = ||F_{t} - F_{t-1}||_{L_1}$',
                plot_options=dict(
                    linestyle='-',
                    color='blue',
                    linewidth=2.0,
                ),
                filter=sad_filter
            ),

            # dict(
            #     name='$D_{{\,{size},t}} '
            #          '= sw\_norm_{{\,{size} }} D_{{t}}$'.format(
            #         size=100
            #     ),
            #     plot_options=dict(
            #         linestyle='-',
            #         color='green',
            #         linewidth=1.0,
            #     ),
            #     filter=sad_filter | sw_vote_norm
            # ),

            # dict(
            #     # The threshold value.
            #     name='$T_{{const}} = {} \in (0; 1)$'.format(
            #         self.THRESHOLD),
            #     plot_options=dict(
            #         linestyle='-',
            #         color='black',
            #         linewidth=2.0,
            #     ),
            #     filter=norm(l=1) | self.THRESHOLD,
            # ),
        )
