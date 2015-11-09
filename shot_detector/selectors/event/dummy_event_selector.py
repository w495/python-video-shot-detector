# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os

from shot_detector.utils.collections import SmartDict

from shot_detector.features.filters import BaseFilter, Filter, \
    DifferenceSWFilter, ZScoreZeroSWFilter, MaxSWFilter, \
    MeanSWFilter, FactorFilter, NormFilter, DeviationDifferenceSWFilter, \
    ZScoreSWFilter, DeviationSWFilter, HistSimpleSWFilter, MedianSWFilter, BoundFilter, \
    StdSWFilter
from shot_detector.features.norms import L1Norm, L2Norm
from shot_detector.handlers import BaseEventHandler, BasePlotHandler

import datetime


diff_filter = Filter(
    sequential_filter_list=[
        Filter(
            name='$F_i = |f_i|_{L_1}$',
            plot_options=SmartDict(
                linestyle='-',
                color='black',
                linewidth=1.0,
            ),
            sequential_filter_list=[
                NormFilter(
                    norm_function=L1Norm.length
                ),
            ],
        ),
        Filter(
            name='DIFF',
            plot_options=SmartDict(
                linestyle='-',
                color='brown',
                linewidth=2.0,
            ),
            sequential_filter_list=[
                DeviationDifferenceSWFilter(
                    window_size=5,
                    std_coef=0,
                ),
                NormFilter(
                    use_abs=True,
                    norm_function=L1Norm.length
                ),
            ],
        ),
    ]
)

class DummyEventSelector(BaseEventHandler):

    __logger = logging.getLogger(__name__)

    cumsum = 0

    plain_plot = BasePlotHandler()
    diff_plot = BasePlotHandler()

    def plot(self, event, video_state, plotter, main_filter):
        for filter_number, filter_desc in enumerate(main_filter.sequential_filter_list):
            offset = filter_desc.get('offset', 0)
            filtered, video_state = filter_desc.filter(
                features=event.features,
                video_state=video_state,
            )
            time = event.time if event.time else 0

            if filtered is not None:
                plotter.add_data(
                    filter_desc.name,
                    1.0 * (time - offset),
                    1.0 * filtered,
                    filter_desc.get('plot_slyle', ''),
                    **filter_desc.get('plot_options', {})
                )

        # if 1.0 <= event.minute:
        #     plotter.plot_data()
        #     return

    def select_event(self, event, video_state=None, *args, **kwargs):

        """
            Should be implemented
        """

        point_flush_trigger = 'point_flush_trigger'
        event_flush_trigger = 'event_flush_trigger'

        self.plot(event, video_state, self.diff_plot, diff_filter)

        now_datetime = datetime.datetime.now()
        diff_time = now_datetime - video_state.start_datetime
        print('  %s -- {%s}; [%s] %s' % (
            diff_time,
            event.number,
            event.hms,
            event.time,
        ))

        return [event], video_state

