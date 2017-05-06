# -*- coding: utf8 -*-
"""
    The illustration different types of video-filters.
    This module shows how to build Frame Difference 
    Rescaling Normalization.
    
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
from shot_detector.charts.event.base import (
    BaseEventChart,
    FilterDescription,
    PlotOptions
)
from shot_detector.utils.log_meta import log_method_call_with


class RescalingEventChart(BaseEventChart):
    """
        Chart for Rescaling Normalization for Frame Difference.
        
        **Algorithm:**
        
            1.  Choose the size of the sliding window 
                (the delay vector).
            2. For each frame from the sequence:
                2.1 Calculate the maximum and minimum value 
                    of the difference in frames on this window.
                2.2 Calculate the range of differences 
                    for a given sliding window.
                2.3 Subtract the minimum value of the difference 
                    from the current value of the difference 
                    between neighboring frames, 
                    and divide it by the range.
            3.  In this way, we get the framed value 
                of the difference in frames for 
                a given sliding window.
            
        **Advantages**:
        
            relative threshold value:
            
                * no need to select for each case;
                * you can use the same value everywhere.
                
        **Disadvantages**:
        
            you need to select the window size:
            
                * with a small window size — got spurious noise;
                * with a large amount — skip the fault.             
                    
                    
        :
    """
    __logger = logging.getLogger(__name__)

    THRESHOLD = 0.8
    SLIDING_WINDOW_SIZE = 400

    @log_method_call_with(logging.WARN)
    def seq_filters(self):
        """
            Returns filter chart options.
    
            What we do:
                1. Declare «builtin» filters.
                2. Build custom filters.
                3. Build target filter.
                4. Plot them with `FilterDescription`
    
            :returns: filter descriptions for rescaling normalization.
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

        # Abstract sliding window. Builtin filter.
        sw = BaseSWFilter(
            size=self.SLIDING_WINDOW_SIZE,
            min_size=2
        )

        # Sliding window that returns maximum.
        sw_max = sw | max

        # Sliding window that returns minimum.
        sw_min = sw | min

        # Sum of absolute difference filter.
        sad_filter = diff | abs | norm(l=1)

        # Range normalization.
        sw_norm = (original - sw_min) / (sw_max - sw_min)

        # Frame difference rescaling normalization by span.
        rescaling_filter = sad_filter | sw_norm

        return [
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
                # Rescaling Normalization by Span.
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
                formula=rescaling_filter
            ),
            FilterDescription(
                # Sum of absolute difference filter.
                name='$D_{t} = ||F_{t} - F_{t-1}||_{L_1}$',
                plot_options=PlotOptions(
                    style='-',
                    color='blue',
                    width=2.0,
                ),
                formula=sad_filter | norm(l=1)
            ),
            FilterDescription(
                # rescaling filter > threshold.
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
                formula=rescaling_filter | threshold
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
