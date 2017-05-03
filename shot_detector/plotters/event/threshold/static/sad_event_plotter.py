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
)
from shot_detector.plotters.event.base import (
    BaseEventPlotter,
    FilterDescription,
    PlotOptions
)

from shot_detector.utils.log_meta import log_method_call_with


class SadEventPlotter(BaseEventPlotter):
    __logger = logging.getLogger(__name__)

    THRESHOLD = 0.08

    @log_method_call_with(logging.INFO)
    def seq_filters(self):
        """
        Returns the sequence of dict in which options of each chart
        are described.
        """
        delay = DelayFilter()
        norm = NormFilter()
        shift = ShiftSWFilter()
        original = delay(0)
        diff = original - shift
        threshold = original > self.THRESHOLD
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
                filter=norm(l=1),
            ),
            FilterDescription(
                # Sum of absolute difference filter.
                name='$D_{t} = ||F_{t} - F_{t-1}||_{L_1}$',
                plot_options=PlotOptions(
                    style='-',
                    color='blue',
                    width=2.0,
                ),
                filter=sad_filter
            ),
            FilterDescription(
                # Sum of absolute difference filter > threshold.
                name='$D_{t} > T_{const} $',
                plot_options=PlotOptions(
                    style=':',
                    color='green',
                    width=2.0,
                ),
                filter=sad_filter | threshold
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
                filter=norm(l=1) | self.THRESHOLD,
            ),
        )
