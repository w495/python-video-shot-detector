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

from shot_detector.filters import (
    Filter,
    ShiftSWFilter,
    DelayFilter,
    NormFilter,
    ModulusFilter,
    MedianSWFilter,
)
from shot_detector.plotters.event.base import (
    BaseEventPlotter,
    FilterDescription,
    PlotOptions
)
from shot_detector.utils.log_meta import log_method_call_with


class ChiRescalingEventPlotter(BaseEventPlotter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    @log_method_call_with(logging.WARN)
    def seq_filters(self):
        """
        
        :return: 
        """
        delay = DelayFilter()
        norm = NormFilter()
        modulus = ModulusFilter()
        shift = ShiftSWFilter()
        original = delay(0)
        diff = original - shift
        # noinspection PyPep8Naming
        T_CONST = 0.8
        # noinspection PyPep8Naming,PyUnusedLocal
        S_CONST = 100
        # noinspection PyUnusedLocal
        threshold = original > T_CONST
        # noinspection PyUnusedLocal
        mean = MedianSWFilter(
            size=200
        )

        # noinspection PyUnusedLocal
        median = MedianSWFilter(
            size=200
        )

        sad_filter = norm(l=1) | diff | modulus

        def pow_2(x):
            """
            
            :param x: 
            :return: 
            """
            return x * x

        d_chi = (diff | pow_2) / (Filter.join(original, shift) | max)

        return (
            FilterDescription(
                # Original signal.
                name='$F_{L_1} = |F_{t}|_{L_1}$',
                plot_options=PlotOptions(
                    style='-',
                    color='gray',
                    width=3.0,
                ),
                formula=norm(l=1),
            ),

            FilterDescription(
                # Original signal.
                name='$F_{L_1} d_chi = |F_{t}|_{L_1}$',
                plot_options=PlotOptions(
                    style='-',
                    color='red',
                    width=3.0,
                ),
                formula=norm(l=1) | d_chi,
            ),

            # FilterDescription(
            #     name='$D_{{\,{size},t}} '
            #          '= swnorm_{{\,{size} }} D_{{t}}$'.format(
            #         size=S_CONST
            #     ),
            #     plot_options=dict(
            #         linestyle='-',
            #         color='green',
            #         linewidth=1.0,
            #     ),
            #     filter=sad_filter | norm(l=1) | swnorm
            # ),

            FilterDescription(
                name='$D_{t} = |F_{t} - F_{t-1}|_{L_1}$',
                plot_options=PlotOptions(
                    style='-',
                    color='blue',
                    width=2.0,
                ),
                formula=sad_filter | norm(l=1)
            ),

            # FilterDescription(
            #     # The threshold value.
            #     name='$T_{{const}} = {} \in (0; 1)$'.format(T_CONST),
            #     plot_options=dict(
            #         linestyle='-',
            #         color='black',
            #         linewidth=2.0,
            #     ),
            #     filter=norm(l=1) | T_CONST,
            # ),
        )
