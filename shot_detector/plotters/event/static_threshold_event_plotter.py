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
    # MaxSWFilter,
    # MinSWFilter,
    # NormSWFilter,
)
from shot_detector.utils.collections import SmartDict
from shot_detector.utils.log_meta import log_method_call_with
from .base_event_plotter import BaseEventPlotter


class StaticThresholdEventPlotter(BaseEventPlotter):

    __logger = logging.getLogger(__name__)

    @log_method_call_with(logging.WARN)
    def seq_filters(self):
        delay = DelayFilter()
        norm = NormFilter()
        modulus = ModulusFilter()
        shift = ShiftSWFilter()
        original = delay(0)
        diff = original - shift
        T_CONST = 0.08
        threshold = original > T_CONST

        sad_filter = diff | modulus

        return (
            SmartDict(
                # Original signal.
                name='$F_{L_1} = |F_{t}|_{L_1}$',
                plot_options=SmartDict(
                    linestyle='-',
                    color='gray',
                    linewidth=3.0,
                ),
                filter=norm(l=1),
            ),
           SmartDict(
               # Sum of absolute differense filter
                name='$D_{t} = |F_{t} - F_{t-1}|_{L_1}$',
                plot_options=SmartDict(
                    linestyle='-',
                    color='blue',
                    linewidth=2.0,
                ),
                filter=sad_filter | norm(l=1)
            ),

           SmartDict(
               # Sum of absolute differense filter > threshold
                name='$D_{t} > T_const $',
                plot_options=SmartDict(
                    linestyle=':',
                    color='green',
                    linewidth=2.0,
                ),
                filter=sad_filter | norm(l=1) | threshold
            ),
            SmartDict(
                name='$T_{const} = 0.8 \in (0; 1)$',
                plot_options=SmartDict(
                    linestyle='-',
                    color='black',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | T_CONST,
            ),
        )
