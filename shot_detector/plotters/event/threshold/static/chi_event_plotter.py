# -*- coding: utf8 -*-

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
from shot_detector.plotters.event.base_event_plotter import \
    BaseEventPlotter
from shot_detector.utils.log_meta import log_method_call_with


class ChiRescalingEventPlotter(BaseEventPlotter):
    __logger = logging.getLogger(__name__)

    @log_method_call_with(logging.WARN)
    def seq_filters(self):
        delay = DelayFilter()
        norm = NormFilter()
        modulus = ModulusFilter()
        shift = ShiftSWFilter()
        original = delay(0)
        diff = original - shift
        T_CONST = 0.8
        S_CONST = 100
        threshold = original > T_CONST
        mean = MedianSWFilter(
            size=200
        )

        median = MedianSWFilter(
            size=200
        )

        sad_filter = norm(l=1) | diff | modulus

        pow_2 = lambda x: x * x

        d_chi = (diff | pow_2) / (Filter.union(original, shift) | max)

        return (
            dict(
                # Original signal.
                name='$F_{L_1} = |F_{t}|_{L_1}$',
                plot_options=dict(
                    linestyle='-',
                    color='gray',
                    linewidth=3.0,
                ),
                filter=norm(l=1),
            ),

            dict(
                # Original signal.
                name='$F_{L_1} d_chi = |F_{t}|_{L_1}$',
                plot_options=dict(
                    linestyle='-',
                    color='red',
                    linewidth=3.0,
                ),
                filter=norm(l=1) | d_chi,
            ),

            # dict(
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

            dict(
                name='$D_{t} = |F_{t} - F_{t-1}|_{L_1}$',
                plot_options=dict(
                    linestyle='-',
                    color='blue',
                    linewidth=2.0,
                ),
                filter=sad_filter | norm(l=1)
            ),

            # dict(
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
