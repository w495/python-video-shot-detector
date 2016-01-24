# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import itertools
import logging

from shot_detector.features.filters import Filter, ShiftSWFilter, LevelSWFilter, \
    MeanSWFilter, NormFilter, DeviationDifferenceSWFilter, \
    StdSWFilter, DecisionTreeRegressorSWFilter, AbsFilter, DCTFilter, DHTFilter

from shot_detector.handlers import BaseEventHandler, BasePlotHandler
from shot_detector.utils.collections import SmartDict

original = Filter()

norm = NormFilter(
)

fabs = AbsFilter()


dct = DCTFilter()

dht = DHTFilter()


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
    window_size=25,
)

mean = MeanSWFilter(
    window_size=10,
)

dtr = DecisionTreeRegressorSWFilter(
    window_size=50,
    strict_windows=True,
    overlap_size=0,
)



sad = original - shift

seq_filters = [

    SmartDict(
        name='$F_i = |f_i|_{L_1}$',
        plot_options=SmartDict(
            linestyle='-',
            color='black',
            linewidth=1.0,
        ),
        filter=norm(l=1),
    ),

    SmartDict(
        name='$F_i DCT = |f_i|_{L_1}$',
        plot_options=SmartDict(
            linestyle='-',
            color='red',
            linewidth=1.0,
        ),
        filter=dct | norm(l=2),
    ),

    SmartDict(
        name='$F_i DHT = |f_i|_{L_1}$',
        plot_options=SmartDict(
            linestyle='-',
            color='blue',
            linewidth=1.0,
        ),
        filter=dht | norm(l=2),
    ),

    # SmartDict(
    #     name='$R_{53} = DTR_{53,1}(F_i)$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter=norm | dtr(s=53, d=1),
    # ),
    #
    # SmartDict(
    #     name='$R_{47} = DTR_{47,1}(F_i)$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='orange',
    #         linewidth=1.0,
    #     ),
    #     filter=norm | dtr(s=47, d=1),
    # ),

    SmartDict(
        name='$level_{10}(|F_i - F_j|)$',
        plot_options=SmartDict(
            linestyle='-',
            color='brown',
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
    #            | (dtr(s=47, d=1) | sad).i(dtr(s=53, d=1) | sad)
    #            | fabs | level,
    # ),
]


class BaseEventSelector(BaseEventHandler):
    __logger = logging.getLogger(__name__)

    cumsum = 0

    plotter = BasePlotHandler()

    def plot(self, aevent_seq, plotter, filter_seq):

        """

        :param aevent_seq:
        :param plotter:
        :param filter_seq:
        """
        f_count = len(filter_seq)
        event_seq_tuple = itertools.tee(aevent_seq, f_count + 1)
        for filter_desc, event_seq in itertools.izip(
            filter_seq,
            event_seq_tuple[1:]
        ):
            offset = filter_desc.get('offset', 0)
            new_event_seq = filter_desc\
                .get('filter')\
                .filter_objects(event_seq)
            for event in new_event_seq:
                filtered = event.feature
                time = event.time if event.time else 0
                plotter.add_data(
                    filter_desc.get('name'),
                    1.0 * (time - offset),
                    1.0 * filtered,
                    filter_desc.get('plot_style', ''),
                    **filter_desc.get('plot_options', {})
                )
        self.__logger.debug('plotter.plot_data() enter')
        plotter.plot_data()
        self.__logger.debug('plotter.plot_data() exit')
        return event_seq_tuple[0]


    def filter_events(self, event_seq, **kwargs):

        """
            Should be implemented
            :param event_seq: 
        """
        event_seq = self.limit_seq(event_seq, 1)

        self.__logger.debug('plot enter')
        event_seq = self.plot(event_seq, self.plotter, seq_filters)
        self.__logger.debug('plot exit')

        #
        # filter = sad | fabs | norm | level(n=10)
        #
        # # event_seq = self.log_seq(event_seq, 'before')
        #
        # event_seq = filter.filter_objects(event_seq)
        #
        # event_seq = itertools.ifilter(lambda item: item.feature > 0.0,
        #                                    event_seq)
        #
        # event_seq = self.log_seq(event_seq, '-> {item} {item.feature}')
        #

        #
        #event_seq = self.log_seq(event_seq)
        #
        #
        # event_seq = itertools.ifilter(lambda x: x>0,
        #                                    event_seq)


        return event_seq
