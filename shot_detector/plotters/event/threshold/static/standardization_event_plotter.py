# -*- coding: utf8 -*-

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging

from shot_detector.filters import (
    ShiftSWFilter,
    DelayFilter,
    NormFilter,
    ModulusFilter,
    BaseSWFilter,
    MeanSWFilter,
    StdSWFilter,
)
from shot_detector.plotters.event.base_event_plotter import \
    BaseEventPlotter
from shot_detector.utils.log_meta import log_method_call_with


class StandardizationEventPlotter(BaseEventPlotter):
    __logger = logging.getLogger(__name__)

    @log_method_call_with(logging.WARN)
    def seq_filters(self):
        T_CONST = 0.8
        S_CONST = 300

        delay = DelayFilter()
        norm = NormFilter()
        modulus = ModulusFilter()
        shift = ShiftSWFilter()

        mean = MeanSWFilter(size=S_CONST)
        std = StdSWFilter(size=S_CONST)

        original = delay(0)
        diff = original - shift

        threshold = original > T_CONST

        sad_filter = diff | modulus

        sw = BaseSWFilter(size=S_CONST, min_size=2)

        swmax = sw | max
        swmin = sw | min

        swnorm = (original - swmin) / (swmax - swmin)

        standardization = (original - mean) / std | abs

        res = standardization

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
                name='$D_{{\,{size},t}} '
                     '= swnorm_{{\,{size} }} D_{{t}}$'.format(
                    size=S_CONST
                ),
                plot_options=dict(
                    linestyle='-',
                    color='green',
                    linewidth=1.0,
                ),
                filter=sad_filter | norm(l=1) | res
            ),

            dict(
                name='$D_{t} = |F_{t} - F_{t-1}|_{L_1}$',
                plot_options=dict(
                    linestyle='-',
                    color='blue',
                    linewidth=2.0,
                ),
                filter=sad_filter | norm(l=1)
            ),

            dict(
                # The threshold value.
                name='$T_{{const}} = {} \in (0; 1)$'.format(T_CONST),
                plot_options=dict(
                    linestyle='-',
                    color='black',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | T_CONST,
            ),
        )
