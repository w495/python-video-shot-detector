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
)

from shot_detector.utils.log_meta import log_method_call_with
from .base_event_plotter import BaseEventPlotter


class StaticThresholdEventPlotter(BaseEventPlotter):
    __logger = logging.getLogger(__name__)

    @log_method_call_with(logging.INFO)
    def seq_filters(self):
        """
        Returns the sequence of dict in which options of each chart
        are described.
        """
        delay = DelayFilter()
        norm = NormFilter()
        modulus = ModulusFilter()
        shift = ShiftSWFilter()
        original = delay(0)
        diff = original - shift
        T_CONST = 0.08
        threshold = original > T_CONST
        sad_filter = diff | modulus | norm(l=1)

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
                # Sum of absolute differense filter.
                name='$D_{t} = |F_{t} - F_{t-1}|_{L_1}$',
                plot_options=dict(
                    linestyle='-',
                    color='blue',
                    linewidth=2.0,
                ),
                filter=sad_filter
            ),
            dict(
                # Sum of absolute differense filter > threshold.
                name='$D_{t} > T_const $',
                plot_options=dict(
                    linestyle=':',
                    color='green',
                    linewidth=2.0,
                ),
                filter=sad_filter | threshold
            ),
            dict(
                # The threshold value.
                name='$T_{const} = 0.8 \in (0; 1)$',
                plot_options=dict(
                    linestyle='-',
                    color='black',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | T_CONST,
            ),
        )
