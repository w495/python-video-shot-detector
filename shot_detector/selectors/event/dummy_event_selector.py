# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os

from shot_detector.utils.collections import SmartDict

from shot_detector.features.filters import BaseFilter, Filter, FilterDifference, LevelSWFilter, \
    DifferenceSWFilter, ZScoreZeroSWFilter, MaxSWFilter, \
    MeanSWFilter, FactorFilter, NormFilter, DeviationDifferenceSWFilter, \
    ZScoreSWFilter, DeviationSWFilter, HistSimpleSWFilter, MedianSWFilter, BoundFilter, \
    StdSWFilter
from shot_detector.features.norms import L1Norm, L2Norm
from shot_detector.handlers import BaseEventHandler, BasePlotHandler

import datetime

norma = NormFilter(
    norm_function=L1Norm.length
)

nabs = NormFilter(
    norm_function=L1Norm.length,
    use_abs=True
)

win_diff = DeviationDifferenceSWFilter(
    window_size=5,
    std_coef=0,
)

ewma_20 = MeanSWFilter(
    window_size=20,
    mean_name='EWMA'
)

ewma_40 = MeanSWFilter(
    window_size=60,
    mean_name='EWMA'
)

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
                norma()
            ],
        ),
        Filter(
            name='$X_i = |f_i|_{L_1}$',
            plot_options=SmartDict(
                linestyle='-',
                color='violet',
                linewidth=1.0,
            ),
            sequential_filter_list=[
                norma(),
                LevelSWFilter(
                    window_size=200,
                )
            ],
        ),

        Filter(
            name='DIFF',
            plot_options=SmartDict(
                linestyle='-',
                color='brown',
            ),
            sequential_filter_list=[
                win_diff,
                norma
            ],
        ),
        Filter(
            name='EWMA_20',
            plot_options=SmartDict(
                linestyle='-',
                color='blue',
            ),
            sequential_filter_list=[
                ewma_20(),
                norma()
            ],
        ),
        Filter(
            name='EWMA_40',
            plot_options=SmartDict(
                linestyle='-',
                color='red',
            ),
            sequential_filter_list=[
                ewma_40(),
                norma()
            ],
        ),
        Filter(
            name='EWMA_40 - EWMA_20',
            plot_options=SmartDict(
                linestyle='-',
                color='green',
            ),
            sequential_filter_list=[
                FilterDifference(
                    parallel_filter_list=[
                        ewma_40(),
                        ewma_20(),
                    ]
                ),
                norma()
            ],
        ),
    ]
)

diff_filter = Filter(
    sequential_filters=[
        # Filter(
        #     name='$F_i = |f_i|_{L_1}$',
        #     plot_options=SmartDict(
        #         linestyle='-',
        #         color='red',
        #         linewidth=1.0,
        #     ),
        #     sequential_filters=[
        #         norma()
        #     ],
        # ),
        Filter(
            name='ewma_20',
            plot_options=SmartDict(
                linestyle='-',
                color='black',
                linewidth=2.0,
            ),
            sequential_filters=[
                ewma_20(),
                norma()
            ],
        ),
    ]
)


class DummyEventSelector(BaseEventHandler):

    __logger = logging.getLogger(__name__)

    cumsum = 0

    plain_plot = BasePlotHandler()
    diff_plot = BasePlotHandler()

    def plot(self, aevent_iterable, plotter, main_filter):

        stream_count = len(main_filter.sequential_filters)
        event_iterables = itertools.tee(aevent_iterable, stream_count)

        for (filter_number, filter_desc), event_iterable in itertools.izip(enumerate(main_filter.sequential_filters), event_iterables):

            self.__logger.debug('filter_number %s starts'%(filter_number))

            offset = filter_desc.get('offset', 0)
            new_event_iterable = filter_desc.filter_objects(event_iterable)
            for event in new_event_iterable:
                filtered = event.feature
                time = event.time if event.time else 0
                plotter.add_data(
                    filter_desc.name,
                    1.0 * (time - offset),
                    1.0 * filtered,
                    filter_desc.get('plot_slyle', ''),
                    **filter_desc.get('plot_options', {})
                )

            self.__logger.debug('filter_number %s end'%(filter_number))


        self.__logger.debug('plotter.plot_data()')

        plotter.plot_data()

        self.__logger.debug('plotter.plot_data() e')



    def __filter_events(self, event_iterable, **kwargs):
        for event in event_iterable:
            if 1.0 > event.minute:
                yield event

    def print_events(self, event_iterable, **kwargs):
        start_datetime = datetime.datetime.now()
        for event in event_iterable:
            # now_datetime = datetime.datetime.now()
            # diff_time = now_datetime - start_datetime
            # print('  %s -- {%s}; [%s] %s' % (
            #     diff_time,
            #     event.number,
            #     event.hms,
            #     event.time,
            # ))
            yield event

    def filter_events(self, event_iterable, **kwargs):

        """
            Should be implemented
        """

        # point_flush_trigger = 'point_flush_trigger'
        # event_flush_trigger = 'event_flush_trigger'
        #


        self.__logger.debug('__filter_events')
        event_iterable = self.__filter_events(event_iterable)


        self.__logger.debug('plot')

        #event_iterable = self.print_events(event_iterable)

        self.plot(event_iterable, self.diff_plot, diff_filter)

        self.__logger.debug('plot e')

        return event_iterable

