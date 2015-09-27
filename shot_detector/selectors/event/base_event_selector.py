# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os

from shot_detector.utils.collections import SmartDict

from shot_detector.features.filters import BaseFilter, \
    MeanSWFilter, LogFilter, NormFilter, DeviationDifferenceSWFilter, \
    ZScoreSWFilter, DeviationSWFilter, FactorFilter, MedianSWFilter, BoundFilter, \
    StdSWFilter
from shot_detector.features.norms import L1Norm, L2Norm
from shot_detector.handlers import BaseEventHandler, BasePlotHandler

import datetime



FILTER_LIST = [
    SmartDict(
        skip=False,
        name='$|f_i|_{L_1}$',
        plot_options=SmartDict(
            linestyle='-.',
            color='gray',
            linewidth=1.0,
        ),
        subfilter_list=[
            (
                NormFilter(), SmartDict(
                    norm_function=L1Norm.length
                ),
            ),
            # (
            #     FactorFilter(), dict(
            #         factor=0.0007,
            #     )
            # ),
        ],
    ),
    SmartDict(
        name='$|f_i|_{L_2}$',
        plot_options=SmartDict(
            linestyle="-",
            color="gray",
            linewidth=1.0,
        ),
        subfilter_list=[
            (
                NormFilter(), SmartDict(
                    norm_function=L2Norm.length
                ),
            ),
            # (
            #     FactorFilter(), dict(
            #         factor=0.015,
            #     )
            # ),
        ],
    ),
    SmartDict(
        skip=False,
        name='$|\log_{10}(f_i)|_{L_2} $',
        plot_slyle=':',
        plot_options=SmartDict(
            linestyle=':',
            color='gray',
            linewidth=1.0,
        ),
        subfilter_list=[
            (
                LogFilter(), SmartDict(),
            ),
            (
                NormFilter(), SmartDict(
                    norm_function=L1Norm.length
                ),
            ),
            # (
            #     FactorFilter(), dict(
            #         factor=0.4,
            #     )
            # ),
        ],
    ),
    SmartDict(
        skip=False,
        name='$|\sigma_{w_{10}} (f_{j})|_{L_2} $',
        plot_slyle='',
        plot_options=SmartDict(
            linestyle="-",
            color="orange",
            linewidth=1.0,
        ),
        subfilter_list=[
            (
                StdSWFilter(), dict(
                    window_size=10,
                    flush_limit=-1,
                    window_limit=-1,
                    flush_trigger='point_flush_trigger',
                )
            ),
            (
                NormFilter(), dict(
                    norm_function=L1Norm.length
                )
            ),
        ],
    ),
    SmartDict(
        skip=False,
        name='$|f_i - f_{i-1}|_{L_2}$',
        plot_slyle='',
        plot_options=SmartDict(
            linestyle="-",
            color="blue",
            linewidth=1.0,
        ),
        subfilter_list=[
            (
                DeviationDifferenceSWFilter(), dict(
                    sigma_num=0,
                    window_size=1,
                    flush_limit=-1,
                    window_limit=-1,
                    flush_trigger='point_flush_trigger',
                )
            ),
            (
                NormFilter(), dict(
                    norm_function=L1Norm.length
                )
            ),
            # (
            #     FactorFilter(), dict(
            #         factor=0.2,
            #     )
            # ),
        ],
    ),
    SmartDict(
        skip=True,
        name='$|\mu(f_i - f_{i-1})|_{L_2}$',
        plot_slyle='',
        plot_options=SmartDict(
            linestyle="-",
            color="brown",
            linewidth=2.0,
        ),
        subfilter_list=[
            (
                DeviationDifferenceSWFilter(), dict(
                    sigma_num=0,
                    window_size=1,
                    flush_limit=-1,
                    window_limit=-1,
                    flush_trigger='point_flush_trigger',
                )
            ),
            (
                MedianSWFilter(), dict(
                    window_size=10,
                    flush_limit=-1,
                    window_limit=-1,
                    flush_trigger='point_flush_trigger',
                )
            ),
            (
                NormFilter(), dict(
                    norm_function=L1Norm.length
                )
            ),
            # (
            #     FactorFilter(), dict(
            #         factor=0.2,
            #     )
            # ),
        ],
    ),
    SmartDict(
        skip=True,
        name='$|\sigma_{w_{10}}(f_i - f_{i-1})|_{L_2}$',
        plot_slyle='',
        plot_options=SmartDict(
            linestyle="-",
            color="red",
            linewidth=1.0,
        ),
        subfilter_list=[
            (
                DeviationDifferenceSWFilter(), dict(
                    sigma_num=0,
                    window_size=1,
                    flush_limit=-1,
                    window_limit=-1,
                    flush_trigger='point_flush_trigger',
                )
            ),
            (
                StdSWFilter(), dict(
                    window_size=10,
                    flush_limit=-1,
                    window_limit=-1,
                    flush_trigger='point_flush_trigger',
                )
            ),
            (
                NormFilter(), dict(
                    norm_function=L1Norm.length
                )
            ),
        ],
    ),
    SmartDict(
        skip=True,
        name='$|\mu_{w_{10}}(\sigma_{w_{10}}(f_i - f_{i-1}))|_{L_2}$',
        plot_options=SmartDict(
            linestyle="-",
            color="green",
            linewidth=1.0,
        ),
        subfilter_list=[
            (

                DeviationDifferenceSWFilter(), dict(
                    sigma_num=0,
                    window_size=1,
                    flush_limit=-1,
                    window_limit=-1,
                    flush_trigger='point_flush_trigger',
                )
            ),
            (
                StdSWFilter(), dict(
                    window_size=10,
                    flush_limit=-1,
                    window_limit=-1,
                    flush_trigger='point_flush_trigger',
                )
            ),
            (
                MeanSWFilter(), dict(
                    window_size=10,
                    flush_limit=-1,
                    window_limit=-1,
                    flush_trigger='point_flush_trigger',
                )
            ),
            (
                NormFilter(), dict(
                    norm_function=L1Norm.length
                )
            ),
        ],
    ),


]


class BaseEventSelector(BaseEventHandler, BasePlotHandler):
    __logger = logging.getLogger(__name__)

    point_data = []

    event_data = []

    def select_event(self, event, video_state=None, *args, **kwargs):

        """
            Should be implemented
        """

        point_flush_trigger = 'point_flush_trigger'
        event_flush_trigger = 'event_flush_trigger'

        if 3 > event.time > 103:
            return event, video_state

        for filter_desc in FILTER_LIST:
            if filter_desc.get('skip'):
                continue
            base_filter = BaseFilter()
            filtered, video_state = base_filter.apply_subfilters(
                subfilter_list=filter_desc.subfilter_list,
                features=event.features,
                video_state=video_state,
            )
            plot_slyle = filter_desc.get('plot_slyle', '')
            plot_options = filter_desc.get('plot_options', {})
            self.add_data(filter_desc.name, event.time, filtered, plot_slyle, **plot_options)


        now_datetime = datetime.datetime.now()

        diff_time = now_datetime - video_state.start_datetime

        #print (event)
        print('  %s -- [%s] %s; t = %s' % (
            diff_time,
            event.hms,
            event.number,
            event.time,
        ))

        if 100 <= event.time <= 101:
            self.plot_data()

        return [event], video_state
