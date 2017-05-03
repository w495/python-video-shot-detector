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
    StdSWFilter,
    DecisionTreeRegressorSWFilter

)
from shot_detector.utils.collections import SmartDict
from .base_event_selector import BaseEventSelector


class DtrEventSelector(BaseEventSelector):
    __logger = logging.getLogger(__name__)

    def seq_filters(self):
        delay = DelayFilter()

        original = delay(0)

        norm = NormFilter()

        shift = ShiftSWFilter(
            window_size=2,
            strict_windows=False,
            cs=False,
        )

        mean = MeanSWFilter(
            window_size=25,
            # strict_windows=True,
            cs=False
        )

        std = StdSWFilter(
            window_size=25,
            strict_windows=True,
        )

        dtr = DecisionTreeRegressorSWFilter(
            window_size=100,
            strict_windows=True,
            overlap_size=0,
            cs=False,
        )

        sad = original - shift

        def sigma3(c=3.0, **kwargs):
            return (
                       original
                       > (
                           mean(**kwargs)
                           + c * std(**kwargs)
                       )
                   ) | int

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
                name='$DTR_{300,2}$',
                plot_options=SmartDict(
                    linestyle='-',
                    color='red',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | dtr(s=300, d=2)
            ),

            SmartDict(
                name='$S_{DTR} = '
                     '\\frac{1}{k}\sum_{i=1}^{k} DTR_{i \cdot 25, 2} $',
                plot_options=SmartDict(
                    linestyle='-',
                    color='green',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | sum(
                    [dtr(s=25 * i + 1) for i in xrange(1, 9)]
                ) / 8
            ),

            SmartDict(
                name='$B_{DTR} = \\frac{1}{k}\sum_{i=1}^{k} '
                     'DTR_{i \cdot 25, 2} $',
                plot_options=SmartDict(
                    linestyle='-',
                    color='magenta',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | sum(
                    [dtr(s=25 * i + 1) for i in xrange(1, 9)]
                ) / 8 | (sad | abs) | sum(
                    sigma3(s=25 * j) for j in xrange(1, 2)
                ) / 8
            ),

            SmartDict(
                name="$V(t)$",
                plot_options=SmartDict(
                    linestyle=':',
                    color='blue',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | sum(
                    dtr(s=25 * i + 1) for i in xrange(1, 9)
                ) / 8 | (sad | abs) | sum(
                    sigma3(s=25 * j) for j in xrange(1, 9)
                ) / 8
            ),
        ]

    def filter_events(self, event_seq, **kwargs):
        """
            Should be implemented
            :param event_seq: 
        """
        event_seq = self.limit_seq(event_seq, 0.0, 2.5)

        self.__logger.debug('plot enter')
        event_seq = self.plot(
            event_seq,
            self.plotter,
            self.seq_filters())
        self.__logger.debug('plot exit')

        return event_seq
