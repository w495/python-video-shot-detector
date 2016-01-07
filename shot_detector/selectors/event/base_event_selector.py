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

#
# PLAIN_FILTER_LIST = [
#     SmartDict(
#         skip=False,
#         name='$F_i = |f_i|_{L_1}$',
#         plot_options=SmartDict(
#             linestyle='-',
#             color='black',
#             linewidth=1.0,
#         ),
#         subfilter_list=[
#             (
#                 NormFilter(), SmartDict(
#                     norm_function=L1Norm.length
#                 ),
#             ),
#         ],
#     ),
#     SmartDict(
#         skip=False,
#         offset=25,
#         name='$M_i = median_{25}(F_j)$',
#         plot_options=SmartDict(
#             linestyle='-',
#             color='gray',
#             linewidth=2.0,
#         ),
#         subfilter_list=[
#             (
#                 DeviationDifferenceSWFilter(), dict(
#                     window_size=2,
#                     std_coef=0,
#                 )
#             ),
#             (
#                 NormFilter(), SmartDict(
#                     norm_function=L1Norm.length
#                 ),
#             ),
#         ],
#     ),
# ]
#
#
# DIFF_FILTER_LIST = [
#
#
#     # SmartDict(
#     #     skip=False,
#     #     name='$F_i = |f_i|_{L_1}$',
#     #     step='MEAN',
#     #     plot_options=SmartDict(
#     #         linestyle='-',
#     #         color='black',
#     #         linewidth=1.0,
#     #     ),
#     #     subfilter_list=[
#     #         (
#     #             NormFilter(), SmartDict(
#     #                 norm_function=L1Norm.length
#     #             ),
#     #         ),
#     #     ],
#     # ),
#
#
#     SmartDict(
#         skip=False,
#         name='DIFF',
#         step = 'DIFF',
#         plot_options=SmartDict(
#             linestyle='-',
#             color='brown',
#             linewidth=2.0,
#         ),
#         subfilter_list=[
#             (
#                 DeviationDifferenceSWFilter(), dict(
#                     window_size=1,
#                     std_coef=0,
#                 )
#             ),
#             (
#                 NormFilter(), SmartDict(
#                     use_abs=True,
#                     norm_function=L1Norm.length
#                 ),
#             ),
#         ],
#     ),
#
#
#     SmartDict(
#         skip=False,
#         name='$S_i = |f_i|_{L_1}$',
#         step = 'STD',
#         plot_options=SmartDict(
#             linestyle='-',
#             color='gray',
#             linewidth=2.0,
#         ),
#         subfilter_list=[
#             # (
#             #     NormFilter(), SmartDict(
#             #         norm_function=L1Norm.length
#             #     ),
#             # ),
#             # (
#             #     MedianSWFilter(), dict(
#             #         window_size=25,
#             #     )
#             # ),
#             (
#                 StdSWFilter(), dict(
#                     window_size=5,
#                     std_coef=0,
#                 )
#             ),
#             # (
#             #     ZScoreZeroSWFilter(), dict(
#             #         sigma_num=2,
#             #     )
#             # ),
#             (
#                 NormFilter(), SmartDict(
#                     use_abs=True,
#                     norm_function=L1Norm.length
#                 ),
#             ),
#         ],
#     ),
#
#
#
#     SmartDict(
#         skip=False,
#         step='E1',
#         name='$DM_1 = |f_j - f_{j-1}|_{L_1}$',
#         plot_options=SmartDict(
#             linestyle='-',
#             color='red',
#             linewidth=1.0,
#         ),
#         subfilter_list=[
#             # (
#             #     NormFilter(), SmartDict(
#             #         norm_function=L1Norm.length
#             #     ),
#             # ),
#             # (
#             #     MedianSWFilter(), dict(
#             #         window_size=10,
#             #     )
#             # ),
#             # (
#             #     StdSWFilter(), dict(
#             #         window_size=25,
#             #         std_coef=0,
#             #     )
#             # ),
#             # (
#             #     NormFilter(), SmartDict(
#             #         use_abs = True,
#             #         norm_function=L1Norm.length,
#             #     ),
#             # ),
#             # (
#             #     ZScoreZeroSWFilter(), dict(
#             #         sigma_num=2,
#             #     )
#             # ),
#             (
#                 MeanSWFilter(), dict(
#                     window_size=5,
#                     mean_name='EWMA'
#                 )
#             ),
#             (
#                 NormFilter(), SmartDict(
#                     use_abs = True,
#                     norm_function=L1Norm.length,
#                 ),
#             ),
#         ],
#     ),
#     SmartDict(
#         skip=False,
#         step='E2',
#         name='$DM_2 = |f_j - f_{j-1}|_{L_1}$',
#         plot_options=SmartDict(
#             linestyle='-',
#             color='orange',
#             linewidth=1.0,
#         ),
#         subfilter_list=[
#             # (
#             #     NormFilter(), SmartDict(
#             #         norm_function=L1Norm.length
#             #     ),
#             # ),
#             # (
#             #     MedianSWFilter(), dict(
#             #         window_size=25,
#             #     )
#             # ),
#             # (
#             #     StdSWFilter(), dict(
#             #         window_size=25,
#             #         std_coef=3,
#             #     )
#             # ),
#             # (
#             #     NormFilter(), SmartDict(
#             #         use_abs = True,
#             #         norm_function=L1Norm.length,
#             #     ),
#             # ),
#             (
#                 MeanSWFilter(), dict(
#                     window_size=20,
#                     mean_name='EWMA'
#                 )
#             ),
#             (
#                 NormFilter(), SmartDict(
#                     use_abs = True,
#                     norm_function=L1Norm.length,
#                 ),
#             ),
#         ],
#     ),
#
#     SmartDict(
#         skip=False,
#         step='E3',
#         name='$DM_3 = |f_j - f_{j-1}|_{L_1}$',
#         plot_options=SmartDict(
#             linestyle='-',
#             color='teal',
#             linewidth=1.0,
#         ),
#         subfilter_list=[
#             # (
#             #     NormFilter(), SmartDict(
#             #         norm_function=L1Norm.length
#             #     ),
#             # ),
#             # (
#             #     MedianSWFilter(), dict(
#             #         window_size=25,
#             #     )
#             # ),
#             # (
#             #     StdSWFilter(), dict(
#             #         window_size=25,
#             #         std_coef=0,
#             #     )
#             # ),
#             # (
#             #     NormFilter(), SmartDict(
#             #         use_abs = True,
#             #         norm_function=L1Norm.length,
#             #     ),
#             # ),
#             (
#                 MeanSWFilter(), dict(
#                     window_size=40,
#                     mean_name='EWMA'
#                 )
#             ),
#             (
#                 NormFilter(), SmartDict(
#                     use_abs = True,
#                     norm_function=L1Norm.length,
#                 ),
#             ),
#         ],
#     ),
#
#     SmartDict(
#         skip=False,
#         step='E1-E2',
#         name='E1-E2',
#         subfilter_list=[],
#     )
# ]
#

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
    level_number=10,
    window_size=100,
    global_max=1.0,
    global_min=0.0,
)

std = StdSWFilter(
    window_size=40,
)

mean = MeanSWFilter(
    window_size=25,
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

    # Filter(
    #     name='$F_i | level$',
    #     plot_options=SmartDict(
    #         #marker='o',
    #         linestyle='-',
    #         color='green',
    #         linewidth=1.0,
    #     ),
    #     filter=l1() | level,
    # ),


    Filter(
        name='$F_i - F_j$',
        plot_options=SmartDict(
            linestyle='-',
            color='brown',
        ),
        filter=mean() | l1(),
    ),
    #
    # Filter(
    #     name='$(F_i - F_j) | level$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='blue',
    #     ),
    #     filter=std | l1_abs() | level,
    # ),

    # Filter(
    #     name='EWMA_20',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='blue',
    #     ),
    #     seq_filters=[
    #         ewma_20(),
    #         l1()
    #     ],
    # ),
    # Filter(
    #     name='EWMA_40',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #     ),
    #     seq_filters=[
    #         ewma_40(),
    #         l1()
    #     ],
    # ),
    # Filter(
    #     name='EWMA_40 - EWMA_20',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='green',
    #     ),
    #     seq_filters=[
    #         FilterDifference(
    #             parallel_filters=[
    #                 ewma_40(),
    #                 ewma_20(),
    #             ]
    #         ),
    #         l1()
    #     ],
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
                    filter_desc.get('plot_slyle', ''),
                    **filter_desc.get('plot_options', {})
                )

        self.__logger.debug('plotter.plot_data()')
        plotter.plot_data()
        self.__logger.debug('plotter.plot_data() e')

    # noinspection PyUnusedLocal
    @staticmethod
    def __filter_events(event_iterable, **_kwargs):
        for event in event_iterable:
            if 2.0 <= event.minute:
                event_iterable.close()
            yield event

    # noinspection PyUnusedLocal
    @staticmethod
    def print_events(event_iterable, **_kwargs):
        # start_datetime = datetime.datetime.now()
        """

        :param event_iterable:
        :param _kwargs:
        """
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
            :param event_iterable: 
        """

        # point_flush_trigger = 'point_flush_trigger'
        # event_flush_trigger = 'event_flush_trigger'
        #

        self.__logger.debug('__filter_events')
        event_iterable = self.__filter_events(event_iterable)

        self.__logger.debug('plot')

        # event_iterable = self.print_events(event_iterable)

        self.plot(event_iterable, self.diff_plot, seq_filters)

        self.__logger.debug('plot e')

        return event_iterable
