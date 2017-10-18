# -*- coding: utf8 -*-
"""
    The illustration different types of video-filters.
    This module shows how to build FFMpeg-like shot detection.
    
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
)
from shot_detector.charts.plot import PlotOptions
from shot_detector.filters import (
    Filter,
    ShiftSWFilter,
    DelayFilter,
    NormFilter,
    # FFMpegLikeThresholdSWFilter
)
from shot_detector.utils.log.log_meta import log_method_call_with
from shot_detector.utils import Qtex

class FfmpegLikeEventChart(BaseEventChart):
    """
        Chart for FFMpeg-like shot detection.
        
        The result of FFMpeg-like filter is the value 
        of the smallest of the two ones:
            1.  The normalized difference brightness 
                of two adjacent frames.
            2.  And the absolute difference 
                of two consecutive differences.
        This minimum is used to avoid surges in case the signal graph 
        decreases or increases monotonically. 
        The difference of two consecutive differences 
        means the speed of brightness changes. 
        The low speed within a significant change indicates 
        that the brightness varies uniformly in some neighborhood 
        of the given frame. While a fast but smooth brightness change 
        there is no disruption.

        You can achieve this FFMpeg-like shot detection 
        directly with ffmpeg:
            
            >$ ffmpeg -i 'file.mp4' \
                -filter:v "select='gt(scene,0.4)',showinfo" \
                -f 'null' \
                -y 'qq' 
    
        But the result wouldn't be the same. The formula 
        and the result are the same as the result of FFmpeg, 
        with an accuracy of FFMPEG_CORRECTION.    
        The correction is due to the fact that in ffmpeg
        Colors represent integers, without normalization.
            
            COLOR_CORRECTION = 3 * 256.0
            
        Coefficients is taken from the source code FFMpeg.
            
            FFMPEG_NORM = 100.0
            FFMPEG_CORRECTION = COLOR_CORRECTION / FFMPEG_NORM
            
        As in the present FFMpeg.
            
            true_ffmpeg = ffmpeg_like * FFMPEG_CORRECTION
        
        **So, what's the problem:**
            1. The threshold value must be known in advance;
            2. You can not use the same value everywhere:
            3. In smooth video — small differences in frames;
            4. In a dynamic video — large frame differences.

        **Ideas:**
            1.  Take into account the video «dynamism»: 
                Scale the difference in frames 
                and normalize in the neighborhood.
            2. Take into account the average value and variance.

    """
    __logger = logging.getLogger(__name__)

    THRESHOLD = 0.08

    @log_method_call_with(logging.INFO)
    def seq_filters(self):
        """
            Returns chart options for FFMpeg-like filter.
    
            What we do:
                1. Declare «builtin» filters.
                2. Build custom filters.
                3. Build target filter.
                4. Plot them with `FilterDescription`
    
            :returns: filter descriptions for FFMpeg-like filter.
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
        threshold = (original > self.THRESHOLD)

        # Sum of absolute difference filter.
        sad_filter = diff | abs | norm(l=1)

        # The absolute difference of two consecutive differences.
        sad_diff_filter = sad_filter | diff | abs

        # The minimum between the difference
        # and the difference in the difference.
        ffmpeg_like = Filter.to_tuple(sad_filter,
                                      sad_diff_filter) | min

        # Faster implementation of FFMpeg-like filter.
        #   ffmpeg_like_fast = FFMpegLikeThresholdSWFilter()

        return (
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
                name='FFMpeg-like filter',
                formula=(
                    ffmpeg_like
                ),
                plot_options=PlotOptions(
                    label=Qtex(
                        'D^{ffmpeg}_{t} = \min(D_t, |D_t-D_{t-1}|)'
                    ),
                    style='solid',
                    color='red',
                    width=2.0,
                ),
            ),
            FilterDescription(
                name='FFMpeg-like discords',
                formula=(
                    # FFMpeg-like filter > threshold.
                    ffmpeg_like | threshold
                ),
                plot_options=PlotOptions(
                    style='dotted',
                    label=Qtex(
                        'D^{ffmpeg}_{t} > T_{const}'
                    ),
                    color='orange',
                    width=2.0,
                ),
            ),
            FilterDescription(
                name='Threshold',
                formula=(
                    norm(l=1) | self.THRESHOLD
                ),
                plot_options=PlotOptions(
                    label=Qtex(
                        "T_{const} = ?{threshold} \in (0; 1)",
                        threshold=self.THRESHOLD
                    ),
                    style='--',
                    color='black',
                    width=2.0,
                ),
            ),
        )
