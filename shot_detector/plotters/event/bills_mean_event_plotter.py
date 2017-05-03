# -*- coding: utf8 -*-

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging

from shot_detector.filters import (
    DelayFilter,
    ShiftSWFilter,
    MeanSWFilter,
    NormFilter,
    SignChangeFilter,
    StdSWFilter,
    ModulusFilter,
    DecisionTreeRegressorSWFilter
)
from shot_detector.utils.collections import SmartDict
from .base_event_plotter import BaseEventPlotter


class BillsMeanEventPlotter(BaseEventPlotter):
    __logger = logging.getLogger(__name__)

    def seq_filters(self):
        print(self.__class__)

        sgn_changes = SignChangeFilter()

        delay = DelayFilter()

        norm = NormFilter()

        modulus = ModulusFilter()

        shift = ShiftSWFilter()

        diff = delay(0) - shift

        mean = MeanSWFilter()

        std = StdSWFilter()

        dtr = DecisionTreeRegressorSWFilter(regressor_depth=2)

        def bill(c=3.0, s=1):
            return (delay(0) > (mean(s=s) + c * std(s=s))) | int

        def mdiff_bill(s=1):
            return (mean(s=s * 2) - mean(s=s)) | sgn_changes

        return [
            SmartDict(
                name='$F_{L_1} = |F_{t}|_{L_1}$',
                plot_options=SmartDict(
                    linestyle='-',
                    color='lightgray',
                    linewidth=3.0,
                ),
                filter=norm(l=1),
            ),

            SmartDict(
                name='$V(t) = '
                     '1/n\sum_{j=1}^{n+1} B_{j \cdot 25} $',
                plot_options=SmartDict(
                    linestyle=':',
                    color='blue',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | sum(
                    mdiff_bill(s=i * 25) for i in xrange(1, 9)
                ) / 8
            ),

            SmartDict(
                name='$V(t) = '
                     '1/n\sum_{j=1}^{n+1} B_{j \cdot 25} $',
                plot_options=SmartDict(
                    linestyle=':',
                    color='blue',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | sum(
                    mdiff_bill(s=i * 25) for i in xrange(1, 9)
                ) / 8 | diff | modulus | sum(
                    bill(s=25 * j) for j in xrange(1, 9)
                ) / 8
            ),
        ]
