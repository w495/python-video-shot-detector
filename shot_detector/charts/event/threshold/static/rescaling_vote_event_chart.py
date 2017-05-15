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

from shot_detector.charts.event.base import (
    BaseEventChart,
    FilterDescription,
)
from shot_detector.charts.plot import PlotOptions
from shot_detector.filters import (
    Filter,
    ShiftSWFilter,
    DelayFilter,
    NormFilter,
    BaseSWFilter,
)
from shot_detector.utils.log_meta import log_method_call_with


class RescalingVoteEventChart(BaseEventChart):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    THRESHOLD = 0.8
    SLIDING_WINDOW_SIZE = 20

    VOTER_COUNT = 16
    VOTER_SIZE = 25

    @log_method_call_with(logging.WARN)
    def seq_filters(self):
        """
            Returns filter chart options.

            What we do:
                1. Declare «builtin» filters.
                2. Build custom filters.
                3. Build target filter.
                4. Plot them with `FilterDescription`

            :returns: filter descriptions for average normalization.
            :rtype: list of FilterDescription
        """

        # Linear delay filter. Builtin filter.
        delay = DelayFilter()

        # The incoming signal is unchanged.
        original = delay(0)

        # Shift signal to one frame. Builtin filter.
        shift = ShiftSWFilter()

        # The difference between neighboring frames.
        diff = original - shift

        # The norm of the signal. Builtin filter.
        norm = NormFilter()

        # Threshold filter.
        # noinspection PyUnusedLocal
        threshold = original > self.THRESHOLD

        # Sum of absolute difference filter.
        sad_filter = diff | abs | norm(l=1)

        # Abstract sliding window. Builtin filter.
        sw = BaseSWFilter(
            size=self.SLIDING_WINDOW_SIZE,
            min_size=2
        )

        # Sliding window that returns maximum.
        sw_max = sw | max

        # Sliding window that returns minimum.
        sw_min = sw | min

        # Range normalization.
        sw_norm = (original - sw_min) / (sw_max - sw_min)

        # Sequence of voters.
        voters = range(self.VOTER_COUNT)

        # Sequence of sliding window sizes.
        sizes = (self.VOTER_SIZE * (i + 1) for i in voters)

        # Sequence of votes of different range normalizations.
        sw_norm_votes_seq = (sw_norm(size=size) for size in sizes)

        # Average vote of different range normalizations.
        sw_vote_norm = Filter.sum(sw_norm_votes_seq) / self.VOTER_COUNT

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
                # Sum of absolute difference filter.
                name='$D_{t} = ||F_{t} - F_{t-1}||_{L_1}$',
                plot_options=PlotOptions(
                    style=':',
                    color='gray',
                    width=1.0,
                ),
                formula=sad_filter
            ),

            FilterDescription(
                # Rescaling normalization with neighborhood size = 100.
                name=(
                    '$D_{{\,{size},t}}'
                    '= sw\_norm_{{\,{size} }} D_{{t}}$'.format(
                        size=100
                    )
                ),
                plot_options=PlotOptions(
                    style='--',
                    color='purple',
                    width=1.0,
                ),
                formula=sad_filter | sw_norm(size=100)
            ),

            FilterDescription(
                # Rescaling normalization with neighborhood size = 200.
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
                # Rescaling normalization with neighborhood size = 300.
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
                # Rescaling normalization with neighborhood size = 400.
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
                # Average vote of different range normalizations.
                name=(
                    '$V_{{\,{size},v,t}} = '
                    '\sum^{{i=v+1}}_{{i=1}} '
                    '\\frac{{ D_{{\,{size} i,t}} }}{{v}};'
                    ' v = {voter_count}$'.format(
                        size=self.VOTER_SIZE,
                        voter_count=self.VOTER_COUNT
                    )
                ),
                plot_options=PlotOptions(
                    style='-',
                    color='green',
                    width=2.0,
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
