# -*- coding: utf8 -*-
"""
    The illustration different types of video-filters.
    This module shows how to build Sum of Absolute Difference filter.
    
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging

from shot_detector.charts.event.base import (
    BaseEventChart,
    FilterDescription,
    PlotOptions
)
from shot_detector.filters import (
    ShiftSWFilter,
    DelayFilter,
    NormFilter,
)
from shot_detector.utils.log_meta import log_method_call_with


class SadEventChart(BaseEventChart):
    """
        Chart for  Sum of Absolute Difference filter.
            
        This is the simplest and most obvious of the possible methods. 
        The result is the value of the normalized per-pixel absolute 
        difference in the luminance of two adjacent frames 
        is used here. The norm is the vector norm L1. 
        
        The physical meaning of SAD is how much one pixel 
        is different from the other. If the average pixel difference 
        exceeds a predetermined number — the threshold, 
        then we think that we have found shot bounding point.
    """

    __logger = logging.getLogger(__name__)

    THRESHOLD = 0.08

    @log_method_call_with(logging.INFO)
    def seq_filters(self):
        """
            Returns chart option sequence for SAD filter illustration.

            What we do:
                1. Declare «builtin» filters.
                2. Build custom filters.
                3. Build target filter.
                4. Plot them with `FilterDescription`

            :returns: filter descriptions for SAD filter.
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
        threshold = original > self.THRESHOLD

        # Sum of absolute difference filter.
        sad_filter = diff | abs | norm(l=1)

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
                    style='-',
                    color='blue',
                    width=2.0,
                ),
                formula=sad_filter
            ),
            FilterDescription(
                # Sum of absolute difference filter > threshold.
                name='$D_{t} > T_{const} $',
                plot_options=PlotOptions(
                    style=':',
                    color='green',
                    width=2.0,
                ),
                formula=sad_filter | threshold
            ),
            FilterDescription(
                # The threshold value.
                name='$T_{{const}} = {threshold} \in (0; 1)$'.format(
                    threshold=self.THRESHOLD
                ),
                plot_options=PlotOptions(
                    style='-',
                    color='black',
                    width=2.0,
                ),
                formula=norm(l=1) | self.THRESHOLD,
            ),
        )
