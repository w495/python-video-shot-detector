# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import itertools
import logging

from shot_detector.features.filters import Filter, ShiftSWFilter, LevelSWFilter, \
    MeanSWFilter, NormFilter, DeviationDifferenceSWFilter, \
    StdSWFilter, DecisionTreeRegressorSWFilter, AbsFilter

from shot_detector.handlers import BaseEventHandler, BasePlotHandler
from shot_detector.utils.collections import SmartDict

original = Filter()

norm = NormFilter()

fabs = AbsFilter()

win_diff = DeviationDifferenceSWFilter(
    window_size=10,
    std_coeff=0,
)

shift = ShiftSWFilter(
    window_size=2,
    strict_windows=False,
)

level = LevelSWFilter(
    level_number=10,
    window_size=1,
    global_max=1.0,
    global_min=0.0,
)

std = StdSWFilter(
    window_size=40,
    strict_windows=True,
)

mean = MeanSWFilter(
    window_size=25,
   # overlap_size=9,
    #strict_windows=True,
    #repeat_windows=True,
)

dtr = DecisionTreeRegressorSWFilter(
    window_size=50,
    strict_windows=True,
    overlap_size=0,
)

hard_mean = MeanSWFilter(
    window_size=50,
    strict_windows=True,
    repeat_windows=True,
    overlap_size=0,
)

mean1 = mean(s=1)


sad = original - shift

seq_filters = [
    SmartDict(
        name='$F_i = |f_i|_{L_1}$',
        plot_options=SmartDict(
            linestyle='-',
            color='gray',
            linewidth=1.0,
        ),
        filter=norm ,
    ),
    SmartDict(
        name='$R_{53} = DTR_{53,1}(F_i)$',
        plot_options=SmartDict(
            linestyle='-',
            color='red',
            linewidth=1.0,
        ),
        filter=norm | dtr(s=53, d=1, j=1),
    ),

    SmartDict(
        name='$R_{47} = DTR_{47,1}(F_i)$',
        plot_options=SmartDict(
            linestyle='-',
            color='orange',
            linewidth=1.0,
        ),
        filter=norm | dtr(s=47, d=1, j=1),
    ),

    SmartDict(
        name='$level_{10}(|F_i - F_j|)$',
        plot_options=SmartDict(
            linestyle='-',
            color='green',
            linewidth=1.0,
        ),
        filter=norm | sad | fabs | level(n=10),
    ),


    # SmartDict(
    #     name='dtr + | sad',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='blue',
    #         linewidth=1.0,
    #     ),
    #     filter=norm
    #            | (
    #                 (dtr(s=47, d=1) | sad).i(dtr(s=53, d=1) | sad)
    #               )
    #            | fabs | level,
    # ),


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
        iterable_tuple = tuple(itertools.tee(aevent_iterable,
                                           stream_count))

        for filter_desc, event_iterable in itertools.izip(sequence_filters, iterable_tuple):

            offset = filter_desc.get('offset', 0)

            new_event_iterable = filter_desc\
                .get('filter')\
                .filter_objects(event_iterable)

            for event in new_event_iterable:
                filtered = event.feature
                time = event.time if event.time else 0
                plotter.add_data(
                    filter_desc.get('name'),
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
            if 0.4 <= event.minute:
                event_iterable.close()
            yield event

    # noinspection PyUnusedLocal
    @staticmethod
    def print_events(event_iterable, string='', **_kwargs):

        import datetime
        start_datetime = datetime.datetime.now()

        """

        :param event_iterable:
        :param _kwargs:
        """

        for event in event_iterable:
            now_datetime = datetime.datetime.now()
            diff_time = now_datetime - start_datetime
            feature = event.feature
            print('  %s  %s -- {%s} {%s} {%s}; [%s] %s %s' % (
                string,
                diff_time,
                event.number,
                event.source.frame_number,
                event.source.packet_number,
                event.hms,
                event.time,
                feature
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

        #event_iterable = self.print_events(event_iterable)

        self.plot(event_iterable, self.diff_plot, seq_filters)

        self.__logger.debug('plot e')

        return event_iterable
