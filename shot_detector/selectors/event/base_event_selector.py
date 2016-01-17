# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import itertools
import logging

from shot_detector.features.filters import BaseFilter, ShiftSWFilter, Filter, LevelSWFilter, \
    MeanSWFilter, NormFilter, DeviationDifferenceSWFilter, \
    StdSWFilter
from shot_detector.features.norms import L1Norm
from shot_detector.handlers import BaseEventHandler, BasePlotHandler
from shot_detector.utils.collections import SmartDict

original = BaseFilter()

l1 = NormFilter(
    norm_function=L1Norm.length
)

l1_abs = NormFilter(
    norm_function=L1Norm.length,
    use_abs=True
)

win_diff = DeviationDifferenceSWFilter(
    window_size=10,
    std_coeff=0,
)

shift = ShiftSWFilter(
    window_size=2,
)

level = LevelSWFilter(
    level_number=4,
    window_size=10,
    overlap_size=9,
    global_max=1.0,
    global_min=0.0,
    strict_windows=True,
    repeat_windows=True
)

std = StdSWFilter(
    window_size=40,
)

mean = MeanSWFilter(
    window_size=25,
    overlap_size=10,
    strict_windows=True,
    repeat_windows=True,
)


sad = original - shift

seq_filters = [
    Filter(
        name='$F_i = |f_i|_{L_1}$',
        plot_options=SmartDict(
            linestyle='-',
            color='black',
            linewidth=1.0,
        ),
        filter=l1(),
    ),

    Filter(
        name='$F_i - F_j$',
        plot_options=SmartDict(
            linestyle='-',
            color='brown',
        ),
        filter=l1 | level ,
    ),
]


class BaseEventSelector(BaseEventHandler):
    __logger = logging.getLogger(__name__)

    cumsum = 0

    plain_plot = BasePlotHandler()
    diff_plot = BasePlotHandler()

    def plot(self, aevent_iterable, plotter, sequence_filters):

        """

        :param aevent_iterable:
        :param plotter:
        :param sequence_filters:
        """
        stream_count = len(sequence_filters)
        iterable_tuple = itertools.tee(aevent_iterable, stream_count)

        for filter_desc, event_iterable in itertools.izip(sequence_filters, iterable_tuple):

            offset = filter_desc.get('offset', 0)

            new_event_iterable = filter_desc.filter.filter_objects(event_iterable)
            for event in new_event_iterable:
                filtered = event.feature
                time = event.time if event.time else 0
                plotter.add_data(
                    filter_desc.name,
                    1.0 * (time - offset),
                    1.0 * filtered,
                    filter_desc.get('plot_style', ''),
                    **filter_desc.get('plot_options', {})
                )

        self.__logger.debug('plotter.plot_data()')
        plotter.plot_data()
        self.__logger.debug('plotter.plot_data() e')

    # noinspection PyUnusedLocal
    @staticmethod
    def __filter_events(event_iterable, **_kwargs):
        for event in event_iterable:
            if 1.0 <= event.minute:
                event_iterable.close()
            yield event

    # noinspection PyUnusedLocal
    @staticmethod
    def print_events(event_iterable, **_kwargs):

        import datetime
        start_datetime = datetime.datetime.now()

        """

        :param event_iterable:
        :param _kwargs:
        """

        for event in event_iterable:
            now_datetime = datetime.datetime.now()
            diff_time = now_datetime - start_datetime
            print('  %s -- {%s} {%s} {%s}; [%s] %s' % (
                diff_time,
                event.number,
                event.source.frame_number,
                event.source.packet_number,
                event.hms,
                event.time,
            ))
            yield event

    def filter_events(self, event_iterable, **kwargs):

        """
            Should be implemented
            :param event_iterable: 
        """

        # point_flush_trigger = 'point_flush_trigger'
        # event_flush_trigger = 'event_flush_trigger'
        #

        self.__logger.debug('__filter_events')
        event_iterable = self.__filter_events(event_iterable)

        self.__logger.debug('plot')

        event_iterable = self.print_events(event_iterable)

        self.plot(event_iterable, self.diff_plot, seq_filters)

        self.__logger.debug('plot e')

        return event_iterable
