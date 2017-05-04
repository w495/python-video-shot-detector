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
from shot_detector.plotters.event.base import (
    BaseEventPlotter,
    FilterDescription,
    PlotOptions
)
from shot_detector.utils.log_meta import log_method_call_with


class StandardizationEventPlotter(BaseEventPlotter):
    __logger = logging.getLogger(__name__)

    @log_method_call_with(logging.WARN)
    def seq_filters(self):
        # noinspection PyPep8Naming
        T_CONST = 0.8
        # noinspection PyPep8Naming
        S_CONST = 300

        delay = DelayFilter()
        norm = NormFilter()
        modulus = ModulusFilter()
        shift = ShiftSWFilter()

        mean = MeanSWFilter(size=S_CONST)
        std = StdSWFilter(size=S_CONST)

        original = delay(0)
        diff = original - shift

        # noinspection PyUnusedLocal
        threshold = original > T_CONST

        sad_filter = diff | modulus

        sw = BaseSWFilter(size=S_CONST, min_size=2)

        sw_max = sw | max
        sw_min = sw | min

        # noinspection PyUnusedLocal
        swnorm = (original - sw_min) / (sw_max - sw_min)

        standardization = (original - mean) / std | abs

        res = standardization

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
                name='$D_{{\,{size},t}} '
                     '= swnorm_{{\,{size} }} D_{{t}}$'.format(
                    size=S_CONST
                ),
                plot_options=PlotOptions(
                    style='-',
                    color='green',
                    width=1.0,
                ),
                formula=sad_filter | norm(l=1) | res
            ),

            FilterDescription(
                name='$D_{t} = |F_{t} - F_{t-1}|_{L_1}$',
                plot_options=PlotOptions(
                    style='-',
                    color='blue',
                    width=2.0,
                ),
                formula=sad_filter | norm(l=1)
            ),

            FilterDescription(
                # The threshold value.
                name='$T_{{const}} = {} \in (0; 1)$'.format(T_CONST),
                plot_options=PlotOptions(
                    style='-',
                    color='black',
                    width=2.0,
                ),
                formula=norm(l=1) | T_CONST,
            ),
        )
