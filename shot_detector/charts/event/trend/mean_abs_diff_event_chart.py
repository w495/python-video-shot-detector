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
    NormFilter,
    BaseSWFilter,
    DelayFilter,
)


class MeanAbsDiffEventChart(BaseEventChart):
    """
        Idea difference between 
        
    """
    __logger = logging.getLogger(__name__)

    def seq_filters(self):
        """
        
        :return: 
        """
        # Linear delay filter. Builtin filter.
        delay = DelayFilter()

        # The incoming signal is unchanged.
        original = delay(0)

        # The norm of the signal. Builtin filter.
        norm = NormFilter()

        # Abstract sliding window. Builtin filter.
        sw = BaseSWFilter(min_size=2)

        sw_mean = sw | numeric.mean
        # or sw_mean = MeanSWFilter()

        return [
            FilterDescription(
                name='$F_{L_1} = |F_{t}|_{L_1}$',
                plot_options=PlotOptions(
                    style='-',
                    color='lightgray',
                    width=3.0,
                ),
                formula=original | norm(l=1),
            ),

            FilterDescription(
                name='$M_{50} = |\hat{\mu}_{50}(F_{L_1})|$',
                plot_options=PlotOptions(
                    style='-',
                    color='orange',
                    width=2.0,
                ),
                formula=norm(l=1) | sw_mean(s=50)
            ),

            FilterDescription(
                name='$M_{100} = |\hat{\mu}_{100}(F_{L_1})|$',
                plot_options=PlotOptions(
                    style='-',
                    color='red',
                    width=2.0,
                ),
                formula=norm(l=1) | sw_mean(s=100)
            ),

            FilterDescription(
                name='$M_{200} = |\hat{\mu}_{200}(F_{L_1})|$',
                plot_options=PlotOptions(
                    style='-',
                    color='blue',
                    width=2.0,
                ),
                formula=norm(l=1) | sw_mean(s=200)
            ),

        ]
