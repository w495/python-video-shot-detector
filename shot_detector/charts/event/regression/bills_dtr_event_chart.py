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
from builtins import range

from shot_detector.charts.event.base import (
    BaseEventChart,
    FilterDescription,
    PlotOptions
)
from shot_detector.filters import (
    DelayFilter,
    ShiftSWFilter,
    MeanSWFilter,
    NormFilter,
    StdSWFilter,
    ModulusFilter,
    DecisionTreeRegressorSWFilter
)


class BillsDtrEventChart(BaseEventChart):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def seq_filters(self):
        """
        
        :return: 
        """
        delay = DelayFilter()

        norm = NormFilter()

        modulus = ModulusFilter()

        shift = ShiftSWFilter()

        diff = delay(0) - shift

        mean = MeanSWFilter()

        std = StdSWFilter()

        dtr = DecisionTreeRegressorSWFilter(regressor_depth=2)

        def bill(c=3.0, s=1):
            """
            
            :param c: 
            :param s: 
            :return: 
            """
            # noinspection PyTypeChecker
            return (delay(0) > (mean(s=s) + c * std(s=s))) | int

        return [
            FilterDescription(
                name='$F_{L_1} = |F_{t}|_{L_1}$',
                plot_options=PlotOptions(
                    style='-',
                    color='lightgray',
                    width=3.0,
                ),
                formula=norm(l=1),
            ),
            FilterDescription(
                name='$DTR_{300,2}$',
                plot_options=PlotOptions(
                    style='-',
                    color='red',
                    width=2.0,
                ),
                formula=norm(l=1) | dtr(s=300, d=2)
            ),
            FilterDescription(
                name='$S = '
                     '1/k\sum_{i=1}^{k+1} DTR_{i \cdot 25, 2} $',
                plot_options=PlotOptions(
                    style='-',
                    color='green',
                    width=2.0,
                ),
                formula=norm(l=1) | sum(
                    dtr(s=25 * i + 1) for i in range(1, 9)
                ) / 8
            ),
            FilterDescription(
                name="$B_{50}/n = "
                     "(|S'| > |(\hat{\mu}_{50} "
                     "+ A \hat{\sigma}_{50})(S')|)"
                     "/n$",
                plot_options=PlotOptions(
                    style='-',
                    color='magenta',
                    width=2.0,
                ),
                formula=norm(l=1) | sum(
                    dtr(s=25 * i + 1) for i in range(1, 9)
                ) / 8 | diff | modulus | bill(s=50) / 8
            ),
            FilterDescription(
                name='$V(t) = '
                     '1/n\sum_{j=1}^{n+1} B_{j \cdot 25} $',
                plot_options=PlotOptions(
                    style=':',
                    color='blue',
                    width=2.0,
                ),
                formula=norm(l=1) | sum(
                    dtr(s=25 * i + 1) for i in range(1, 9)
                ) / 8 | diff | modulus | sum(
                    bill(s=25 * j) for j in range(1, 9)
                ) / 8
            ),
        ]
