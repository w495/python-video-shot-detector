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
from shot_detector.utils.multiprocessing import FuncSeqMapper


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

    def plot(self, src_event_seq, chart, filter_seq):

        """

        :param src_event_seq:
        :param chart:
        :param filter_seq:
        """
        src_event_seq, dst_event_seq  = itertools.tee(src_event_seq)
        processed_seq = self.processed_seq(src_event_seq, filter_seq)

        filter_event = zip(filter_seq, processed_seq)

        for filter_desc, event_seq in filter_event:
            for event in event_seq:
                # self.__logger.info(
                #     "\n<<%s>> - %s - [%s] -<%s>",
                #     filter_desc.name,
                #     event,
                #     event.time,
                #     event.feature
                # )

                filtered = event.feature

                time = 0
                if event.time:
                    time = float(event.time)
                chart.add_data(
                    name=filter_desc.name,
                    key=(1.0 * (time - filter_desc.offset)),
                    value=(1.0 * filtered),
                    plot_options=filter_desc.plot_options
                )

        self.__logger.debug('chart.plot_data() enter')
        chart.plot_data(show=False)
        self.__logger.debug('chart.plot_data() exit')
        return dst_event_seq

    def processed_seq_legacy(self, proc_event_seq, filter_seq):

        def to_list(seq):
            """

            :param seq: 
            :return: 
            """
            return seq

        def apply_filter(arg):
            """

            :param arg: 
            :return: 
            """
            (filter_desc, event_seq) = arg
            filter_objects = filter_desc.formula.filter_objects
            event_seq = filter_objects(event_seq)
            return to_list(event_seq)

        filter_event = self.filter_event(
            proc_event_seq,
            filter_seq
        )
        filter_event_seq = (
            (fd, to_list(es)) for fd, es in filter_event
        )
        processed_seq = map(apply_filter, filter_event_seq)
        return processed_seq

    def processed_seq_simple(self, proc_event_seq, filter_seq):
        event_seq_tuple = self.event_seq_tuple(
            proc_event_seq,
            filter_seq
        )

        filter_event = zip(filter_seq, event_seq_tuple)
        for filter_desc, event_seq in filter_event:
            new_event_seq = self.apply_filter(filter_desc, event_seq)
            yield new_event_seq

    def filter_event(self, proc_event_seq, filter_seq):
        event_seq_tuple = self.event_seq_tuple(
            proc_event_seq,
            filter_seq
        )
        filter_event = zip(filter_seq, event_seq_tuple)
        return filter_event

    def event_seq_tuple(self, proc_event_seq, filter_seq):
        filter_count = len(filter_seq)
        event_seq_tuple = itertools.tee(proc_event_seq, filter_count)
        return event_seq_tuple

    def apply_filter(self, filter_desc, event_seq):
        filter_objects = filter_desc.formula.filter_objects
        events = self.event_seq_to_list(event_seq)
        new_event_seq = filter_objects(events)
        new_events = self.event_seq_to_list(new_event_seq)
        return new_events

    @staticmethod
    def event_seq_to_list(seq):
        """

        :param seq: 
        :return: 
        """
        return seq

    def processed_seq_future(self, proc_event_seq, filter_seq):

        func_seq = list(
            filter_desc.formula.filter_objects_as_list
            for filter_desc in filter_seq
        )

        func_seq_mapper = FuncSeqMapper(
            caller=self
        )

        processed_seq = func_seq_mapper.map(
            func_seq,
            list(proc_event_seq),
        )

        return processed_seq

    def processed_seq(self, proc_event_seq, filter_seq):
        return self.processed_seq_simple(proc_event_seq, filter_seq)
