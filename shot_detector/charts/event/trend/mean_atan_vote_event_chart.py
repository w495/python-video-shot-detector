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
    Filter,
    NormFilter,
    SignChangeFilter,
    ShiftSWFilter,
    BaseSWFilter,
    MeanSWFilter,
    MedianSWFilter,
    SignAngleDiff1DFilter,
    DelayFilter,
    AtanFilter,

)

from operator import mul

class MeanAtanVoteEventChart(BaseEventChart):
    """
        ...
    """
    __logger = logging.getLogger(__name__)


    VOTER_COUNT = 4
    VOTER_SIZE = 25


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

        sw_mean = sw | numeric.mean
        # or sw_mean = MeanSWFilter()

        sw_median = MedianSWFilter(
            size=10
        )



        sw_max = sw | max

        sign_change = SignChangeFilter()

        atan2 = (
            diff
            | original * 256.0
            | numeric.math.atan
            | original * 2 / numeric.math.pi
        )
        # or
        atan = AtanFilter()

        def sw_mean_diff(g, l):
            return (
                norm(l=1)
                | sw_median(s=10)
                | (sw_mean(s=g) - sw_mean(s=l))
                | (sign_change * atan)
            )



        # Sequence of voters.
        voters = range(self.VOTER_COUNT)

        # Sequence of sliding window sizes.
        sizes = list(self.VOTER_SIZE * (i + 1) for i in voters)

        # Sequence of votes of different range normalizations.
        sw_mean_diff_seq = list(
            sw_mean_diff(g=gsize, l=lsize)
            for gsize in sizes
                for lsize in sizes
                    if gsize > lsize
        )



        # Average vote of different range normalizations.
        sw_mean_diff_norm = (
            original
            | sum(sw_mean_diff_seq)
            | original / len(sw_mean_diff_seq)
        )


        return [
            FilterDescription(
                name='$F_{L_1} = |F_{t}|_{L_1}$',
                plot_options=PlotOptions(
                    style='-',
                    color='lightgray',
                    width=3.0,
                ),
                formula=norm(l=1),
            ),

            #
            #
            # FilterDescription(
            #     name='$M_{50} = |\hat{\mu}_{50}(F_{L_1})|$',
            #     plot_options=PlotOptions(
            #         style='-',
            #         color='orange',
            #         width=2.0,
            #     ),
            #     formula=norm(l=1) | sw_mean(s=50)
            # ),
            #
            # FilterDescription(
            #     name='$M_{100} = |\hat{\mu}_{100}(F_{L_1})|$',
            #     plot_options=PlotOptions(
            #         style='-',
            #         color='red',
            #         width=2.0,
            #     ),
            #     formula=norm(l=1) | sw_mean(s=100)
            # ),
            #
            # FilterDescription(
            #     name='$M_{200} = |\hat{\mu}_{200}(F_{L_1})|$',
            #     plot_options=PlotOptions(
            #         style='-',
            #         color='blue',
            #         width=2.0,
            #     ),
            #     formula=norm(l=1) | sw_mean(s=200)
            # ),
            #
            #
            # FilterDescription(
            #     name='$|M_{200} - M_{50}| \\to_{\pm} 0$',
            #     plot_options=PlotOptions(
            #         style='--',
            #         color='blue',
            #         width=1.2,
            #     ),
            #     formula=(
            #         norm(l=1)
            #         | (sw_mean(s=200) - sw_mean(s=50))
            #         # | sign_changes
            #         # | abs
            #         # | original * 0.9
            #     )
            # ),
            #
            #
            # FilterDescription(
            #     name='$M_{50} = |\hat{\mu}_{50}(F_{L_1})|$',
            #     plot_options=PlotOptions(
            #         style='-',
            #         color='orange',
            #         width=2.0,
            #     ),
            #     formula=norm(l=1) | sw_mean(s=50)
            # ),
            #
            #
            #
            # FilterDescription(
            #     name='$M_{50} = |\hat{\mu}_{50}(F_{L_1})|$',
            #     plot_options=PlotOptions(
            #         style='-',
            #         color='orange',
            #         width=2.0,
            #     ),
            #     formula=norm(l=1) | sw_mean(s=50)
            # ),


            # FilterDescription(
            #     name='25',
            #     plot_options=PlotOptions(
            #         style='-',
            #         color='orange',
            #         width=2.0,
            #     ),
            #     formula=norm(l=1) | sw_mean(s=25)
            # ),
            #
            # FilterDescription(
            #     name='50',
            #     plot_options=PlotOptions(
            #         style='-',
            #         color='red',
            #         width=2.0,
            #     ),
            #     formula=norm(l=1) | sw_mean(s=50)
            # ),
            #
            # FilterDescription(
            #     name='75',
            #     plot_options=PlotOptions(
            #         style='-',
            #         color='green',
            #         width=2.0,
            #     ),
            #     formula=norm(l=1) | sw_mean(s=75)
            # ),
            #
            FilterDescription(
                name='100',
                plot_options=PlotOptions(
                    style='-',
                    color='purple',
                    width=2.0,
                ),
                formula=norm(l=1) | sw_mean(s=100)
            ),


            FilterDescription(
                name='$A|M_{200} - M_{100}| \\to_{\pm} 0$',
                plot_options=PlotOptions(
                    style='--',
                    color='blue',
                    width=1.0,
                ),
                formula=norm(l=1) | sw_mean_diff_norm # sw_mean_diff(25,12)
            ),



        ]
