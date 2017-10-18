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
)
from shot_detector.charts.plot import PlotOptions
from shot_detector.filters import (
    BaseSWFilter,
    ShiftSWFilter,
    DelayFilter,
    NormFilter
)

from shot_detector.utils import Qtex

class EstimationDiffEventChart(BaseEventChart):
    """
        ...
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

        def sigma_estimation(sigma=2.0, size=1):
            """

            :param float sigma: 
            :param int size: 
            :return: 
            """
            return sw_mean(s=size) + (sigma * sw_std(s=size))

        def sigma_check(**kwargs):
            """
                ...
            """
            return (original > sigma_estimation(**kwargs)) | int

        return [
            FilterDescription(
                name='L1 filter',
                formula=(
                    norm(l=1)
                ),
                plot_options=PlotOptions(
                    label=Qtex(
                        '||Y_{t}||_{L_1}'
                    ),
                    style='-',
                    color='lightgray',
                    width=4.0,
                ),
            ),

            FilterDescription(
                name='Threshold',
                formula=(
                    norm(l=1)
                    | sigma_estimation(size=200)
                ),
                plot_options=PlotOptions(
                    label=Qtex(
                        "E_{?{size},t} = \overline{Y}_{?{size},t} + 2 \cdot S_{?{size},t}",
                        size=200
                    ),
                    style='-',
                    color='red',
                    width=2.0,
                ),
            ),

            FilterDescription(
                formula=(
                    norm(l=1)
                    | sigma_check(size=100)
                ),
                plot_options=PlotOptions(label=Qtex(
                    "||Y_{t}||_{L_1} > ||E_{?{size},t}||_{L_1}",
                        size=200
                    ),
                    style=':',
                    color='green',
                    width=2.0,
                ),
            ),


        ]
