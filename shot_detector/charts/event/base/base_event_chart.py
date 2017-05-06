# -*- coding: utf8 -*-
"""
    ...
"""

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import itertools
import logging
# PY2 & PY3 — compatibility
from builtins import map, zip

from shot_detector.handlers import BaseEventHandler, BasePlotHandler


class BaseEventChart(BaseEventHandler):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def filter_events(self, event_seq, **kwargs):

        """
            Should be implemented
            :param event_seq:
        """
        event_seq = self.plot_events(event_seq, **kwargs)

        return event_seq

    def plot_events(self, event_seq, **kwargs):
        """
            Should be implemented
            :param event_seq:
        """

        service_options = kwargs['service_options']

        event_seq = self.limit_seq(
            event_seq,
            first=service_options.get('first_frame', 0),
            last=service_options.get('last_frame', 60),
            as_stream=service_options.get('as_stream', False)
        )

        plot_handler = BasePlotHandler(
            options=service_options
        )

        self.__logger.debug('plot enter {}'.format(type(self).__name__))
        event_seq = self.plot(
            event_seq,
            plot_handler,
            self.seq_filters()
        )
        self.__logger.debug('plot exit')

        return event_seq

    def seq_filters(self):
        """
        
        :return: 
        """
        return ()

    def plot(self, aevent_seq, chart, filter_seq):

        """

        :param aevent_seq:
        :param chart:
        :param filter_seq:
        """
        f_count = len(filter_seq)
        event_seq_tuple = itertools.tee(aevent_seq, f_count + 1)

        #
        # process_pool = ProcessPool()

        def to_list(x):
            """
            
            :param x: 
            :return: 
            """
            return x

        def apply_filter(arg, ):
            """
            
            :param arg: 
            :return: 
            """
            (filter_desc, event_seq) = arg

            event_seq = filter_desc.formula.filter_objects(event_seq)
            return to_list(event_seq)

        filter_event = zip(filter_seq, event_seq_tuple[1:])
        filter_event_seq = (
            (filter_desc, to_list(event_seq))
            for filter_desc, event_seq in filter_event
        )

        processed_seq = map(
            apply_filter,
            filter_event_seq
        )

        # process_pool.close()
        for filter_desc, event_seq in zip(
                filter_seq,
                processed_seq
        ):

            for event in event_seq:
                #
                # print (
                #     filter_desc.get('name'),
                #     event,
                #     event.time,
                #     event.feature
                # )
                filtered = event.feature

                time = event.time if event.time else 0
                chart.add_data(
                    name=filter_desc.name,
                    key=(1.0 * (time - filter_desc.offset)),
                    value=(1.0 * filtered),
                    plot_options=filter_desc.plot_options
                )

        self.__logger.debug('chart.plot_data() enter')
        chart.plot_data()
        self.__logger.debug('chart.plot_data() exit')
        return event_seq_tuple[0]
