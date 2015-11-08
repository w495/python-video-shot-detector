# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os

from shot_detector.utils.collections import SmartDict

from shot_detector.features.filters import BaseFilter, \
    DifferenceSWFilter, ZScoreZeroSWFilter, MaxSWFilter, \
    MeanSWFilter, FactorFilter, NormFilter, DeviationDifferenceSWFilter, \
    ZScoreSWFilter, DeviationSWFilter, HistSimpleSWFilter, MedianSWFilter, BoundFilter, \
    StdSWFilter
from shot_detector.features.norms import L1Norm, L2Norm
from shot_detector.handlers import BaseEventHandler, BasePlotHandler

import datetime

PLAIN_FILTER_LIST = [
    SmartDict(
        skip=False,
        name='$F_i = |f_i|_{L_1}$',
        plot_options=SmartDict(
            linestyle='-',
            color='black',
            linewidth=1.0,
        ),
        subfilter_list=[
            (
                NormFilter(), SmartDict(
                    norm_function=L1Norm.length
                ),
            ),
        ],
    ),
    SmartDict(
        skip=False,
        offset=25,
        name='$M_i = median_{25}(F_j)$',
        plot_options=SmartDict(
            linestyle='-',
            color='gray',
            linewidth=2.0,
        ),
        subfilter_list=[
            (
                DeviationDifferenceSWFilter(), dict(
                    window_size=2,
                    std_coef=0,
                )
            ),
            (
                NormFilter(), SmartDict(
                    norm_function=L1Norm.length
                ),
            ),
        ],
    ),
]


DIFF_FILTER_LIST = [


    # SmartDict(
    #     skip=False,
    #     name='$F_i = |f_i|_{L_1}$',
    #     step='MEAN',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='black',
    #         linewidth=1.0,
    #     ),
    #     subfilter_list=[
    #         (
    #             NormFilter(), SmartDict(
    #                 norm_function=L1Norm.length
    #             ),
    #         ),
    #     ],
    # ),


    SmartDict(
        skip=False,
        name='DIFF',
        step = 'DIFF',
        plot_options=SmartDict(
            linestyle='-',
            color='brown',
            linewidth=2.0,
        ),
        subfilter_list=[
            (
                DeviationDifferenceSWFilter(), dict(
                    window_size=1,
                    std_coef=0,
                )
            ),
            (
                NormFilter(), SmartDict(
                    use_abs=True,
                    norm_function=L1Norm.length
                ),
            ),
        ],
    ),


    SmartDict(
        skip=False,
        name='$S_i = |f_i|_{L_1}$',
        step = 'STD',
        plot_options=SmartDict(
            linestyle='-',
            color='gray',
            linewidth=2.0,
        ),
        subfilter_list=[
            # (
            #     NormFilter(), SmartDict(
            #         norm_function=L1Norm.length
            #     ),
            # ),
            # (
            #     MedianSWFilter(), dict(
            #         window_size=25,
            #     )
            # ),
            (
                StdSWFilter(), dict(
                    window_size=5,
                    std_coef=0,
                )
            ),
            # (
            #     ZScoreZeroSWFilter(), dict(
            #         sigma_num=2,
            #     )
            # ),
            (
                NormFilter(), SmartDict(
                    use_abs=True,
                    norm_function=L1Norm.length
                ),
            ),
        ],
    ),



    SmartDict(
        skip=False,
        step='E1',
        name='$DM_1 = |f_j - f_{j-1}|_{L_1}$',
        plot_options=SmartDict(
            linestyle='-',
            color='red',
            linewidth=1.0,
        ),
        subfilter_list=[
            # (
            #     NormFilter(), SmartDict(
            #         norm_function=L1Norm.length
            #     ),
            # ),
            # (
            #     MedianSWFilter(), dict(
            #         window_size=10,
            #     )
            # ),
            # (
            #     StdSWFilter(), dict(
            #         window_size=25,
            #         std_coef=0,
            #     )
            # ),
            # (
            #     NormFilter(), SmartDict(
            #         use_abs = True,
            #         norm_function=L1Norm.length,
            #     ),
            # ),
            # (
            #     ZScoreZeroSWFilter(), dict(
            #         sigma_num=2,
            #     )
            # ),
            (
                MeanSWFilter(), dict(
                    window_size=5,
                    mean_name='EWMA'
                )
            ),
            (
                NormFilter(), SmartDict(
                    use_abs = True,
                    norm_function=L1Norm.length,
                ),
            ),
        ],
    ),
    SmartDict(
        skip=False,
        step='E2',
        name='$DM_2 = |f_j - f_{j-1}|_{L_1}$',
        plot_options=SmartDict(
            linestyle='-',
            color='orange',
            linewidth=1.0,
        ),
        subfilter_list=[
            # (
            #     NormFilter(), SmartDict(
            #         norm_function=L1Norm.length
            #     ),
            # ),
            # (
            #     MedianSWFilter(), dict(
            #         window_size=25,
            #     )
            # ),
            # (
            #     StdSWFilter(), dict(
            #         window_size=25,
            #         std_coef=3,
            #     )
            # ),
            # (
            #     NormFilter(), SmartDict(
            #         use_abs = True,
            #         norm_function=L1Norm.length,
            #     ),
            # ),
            (
                MeanSWFilter(), dict(
                    window_size=20,
                    mean_name='EWMA'
                )
            ),
            (
                NormFilter(), SmartDict(
                    use_abs = True,
                    norm_function=L1Norm.length,
                ),
            ),
        ],
    ),

    SmartDict(
        skip=False,
        step='E3',
        name='$DM_3 = |f_j - f_{j-1}|_{L_1}$',
        plot_options=SmartDict(
            linestyle='-',
            color='teal',
            linewidth=1.0,
        ),
        subfilter_list=[
            # (
            #     NormFilter(), SmartDict(
            #         norm_function=L1Norm.length
            #     ),
            # ),
            # (
            #     MedianSWFilter(), dict(
            #         window_size=25,
            #     )
            # ),
            # (
            #     StdSWFilter(), dict(
            #         window_size=25,
            #         std_coef=0,
            #     )
            # ),
            # (
            #     NormFilter(), SmartDict(
            #         use_abs = True,
            #         norm_function=L1Norm.length,
            #     ),
            # ),
            (
                MeanSWFilter(), dict(
                    window_size=40,
                    mean_name='EWMA'
                )
            ),
            (
                NormFilter(), SmartDict(
                    use_abs = True,
                    norm_function=L1Norm.length,
                ),
            ),
        ],
    ),

    SmartDict(
        skip=False,
        step='E1-E2',
        name='E1-E2',
        subfilter_list=[],
    )
]



class BaseEventSelector(BaseEventHandler):
    __logger = logging.getLogger(__name__)

    cumsum = 0

    plain_plot = BasePlotHandler()
    diff_plot = BasePlotHandler()


    def plot(self, event, video_state, plotter, filter_list):
        for filter_number, filter_desc in enumerate(filter_list):
            if filter_desc.get('skip'):
                continue
            offset = filter_desc.get('offset', 0)
            step = filter_desc.get('step', None)
            base_filter = BaseFilter()
            filtered, video_state = base_filter.apply_subfilters(
                subfilter_list=filter_desc.subfilter_list,
                features=event.features,
                video_state=video_state,
                filter_number = filter_number,
                frame_number = event.number,
            )


            if 'E1' == step:
                self.E1 = filtered
            if 'E2' == step:
                self.E2 = filtered
            if 'E3' == step:
                self.E3 = filtered


            if 'STD' == step:
                self.STD = filtered


            if 'E1-E2' == step:

                #x = ((self.E1 > self.E2) and (self.E2 > self.E3) and ((self.E1 - self.E2) > (self.E2  - self.E3)))


                filtered = abs(self.E1 - self.E2)

                # x = abs(self.E1 - self.E2) > self.STD
                # filtered = -0.5 * x
                # if(filtered  == -0.5):
                #     print  (' event.time = %s %s'%(event.hms, event.number))


            # if filter_desc.name == 'cumsum':
            #     self.cumsum += filtered
            #     filtered = self.cumsum
            #
            #     print ('cs = ', filtered)

            #
            # print ('filtered = ', filtered)

            time = event.time if event.time else 0

            if filtered is not None:
                plotter.add_data(
                    filter_desc.name,
                    1.0 * (time - offset),
                    1.0 * filtered,
                    filter_desc.get('plot_slyle', ''),
                    **filter_desc.get('plot_options', {})
                )



        if 1.0 <= event.minute:
            plotter.plot_data()
            return

    def select_event(self, event, video_state=None, *args, **kwargs):

        """
            Should be implemented
        """

        point_flush_trigger = 'point_flush_trigger'
        event_flush_trigger = 'event_flush_trigger'


        # self.plot(event, video_state, self.plain_plot, PLAIN_FILTER_LIST)
        #

        self.plot(event, video_state, self.diff_plot, DIFF_FILTER_LIST)

        now_datetime = datetime.datetime.now()
        diff_time = now_datetime - video_state.start_datetime
        # print('  %s -- {%s}; [%s] %s' % (
        #     diff_time,
        #     event.number,
        #     event.hms,
        #     event.time,
        # ))

        return [event], video_state
