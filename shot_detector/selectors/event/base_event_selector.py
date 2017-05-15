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
from builtins import zip

from shot_detector.handlers import BaseEventHandler, BasePlotHandler


class BaseEventSelector(BaseEventHandler):
    """
        ...
    """

    __logger = logging.getLogger(__name__)

    chart = BasePlotHandler()

    def plot(self, aevent_seq, chart, filter_seq):

        """

        :param aevent_seq:
        :param chart:
        :param filter_seq:
        """
        f_count = len(filter_seq)
        event_seq_tuple = itertools.tee(aevent_seq, f_count + 1)
        for filter_desc, event_seq in zip(
                filter_seq,
                event_seq_tuple[1:]
        ):
            offset = filter_desc.get('offset', 0)
            new_event_seq = filter_desc \
                .get('filter') \
                .filter_objects(event_seq)
            for event in new_event_seq:
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
                    filter_desc.get('name'),
                    1.0 * (time - offset),
                    1.0 * filtered,
                    filter_desc.get('plot_style', ''),
                    **filter_desc.get('plot_options', {})
                )
        self.__logger.debug('chart.plot_data() enter')
        chart.plot_data()
        self.__logger.debug('chart.plot_data() exit')
        return event_seq_tuple[0]

    def filter_events(self, event_seq, **_):
        """
        Should be implemented
            
        :param event_seq: 
        :param _: 
        :return: 
        """
        event_seq = self.limit_seq(event_seq, 0.0, 1.5)

        self.__logger.debug('plot enter')

        self.__logger.debug('plot exit')

        return event_seq
