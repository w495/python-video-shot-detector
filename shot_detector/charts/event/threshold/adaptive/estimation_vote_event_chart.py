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

import numpy as numeric

from shot_detector.charts.event.base import (
    BaseEventChart,
    FilterDescription,
    PlotOptions
)
from shot_detector.filters import (
    BaseSWFilter,
    ShiftSWFilter,
    DelayFilter,
    NormFilter
)


class EstimationVoteEventChart(BaseEventChart):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    THRESHOLD = 0.8

    VOTER_COUNT = 32
    VOTER_SIZE = 12

    def seq_filters(self):
        """

        :return: 
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

        # Abstract sliding window. Builtin filter.
        sw = BaseSWFilter(min_size=2)

        # Sum of absolute difference filter.
        sad_filter = diff | abs | norm(l=1)

        sw_mean = sw | numeric.mean
        # or sw_mean = MeanSWFilter()

        sw_std = sw | numeric.std

        # or sw_std = StdSWFilter()

        def sigma_estimation(sigma=3.0, size=1):
            """

            :param float sigma: 
            :param int size: 
            :return: 
            """
            return sw_mean(s=size) + sigma * sw_std(s=size)

        def sigma_check(**kwargs):
            """
                ...
            """
            return original > sigma_estimation(**kwargs)

        # Sequence of voters.
        voters = range(self.VOTER_COUNT)

        # Sequence of sliding window sizes.
        sizes = (self.VOTER_SIZE * (i + 1) for i in voters)

        # Sequence of votes of different sizes.
        sigma_vote_seq = (sigma_check(size=size) for size in sizes)

        # Average vote of different sizes.
        sigma_vote = sum(sigma_vote_seq) / self.VOTER_COUNT

        return [
            FilterDescription(
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
                    style='-',
                    color='blue',
                    width=2.0,
                ),
                formula=sad_filter
            ),

            FilterDescription(
                name=(
                    '$D_{{t}} > E_{{ {size} }}\ (D_{{t}})$'.format(
                        size=100
                    )
                ),
                plot_options=PlotOptions(
                    style='--',
                    color='green',
                    width=1.0,
                ),
                formula=(
                    sad_filter
                    | sigma_check(size=100)
                )
            ),
            FilterDescription(
                name=(
                    '$D_{{t}} > E_{{ {size} }}\ (D_{{t}})$'.format(
                        size=200
                    )
                ),
                plot_options=PlotOptions(
                    style='--',
                    color='red',
                    width=1.5,
                    marker='x'
                ),
                formula=(
                    sad_filter
                    | sigma_check(size=200) * 0.8
                )
            ),

            FilterDescription(
                name=(
                    'VOTE'
                ),
                plot_options=PlotOptions(
                    style='-',
                    color='green',
                    width=1.5,
                ),
                formula=(
                    sad_filter
                    | sigma_vote
                )
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

        ]
