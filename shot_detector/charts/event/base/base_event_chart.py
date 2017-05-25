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

from shot_detector.handlers import BaseEventHandler
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

    def plot_events(self,
                    event_seq,
                    first_frame=0,
                    last_frame=60,
                    as_stream=False,
                    plotter=None,
                    **_):
        """
        
        :param event_seq: 
        :param first_frame: 
        :param last_frame: 
        :param as_stream: 
        :param plotter: 
        :param _: 
        :return: 
        """

        event_seq = self.limit_seq(
            event_seq,
            first=first_frame,
            last=last_frame,
            as_stream=as_stream
        )

        plotter = plotter(
            save_name=plotter.save_name.format(
                chart=self.chart_name
            ),
            save_dir=plotter.save_dir.format(
                chart=self.chart_name
            )
        )

        self.__logger.debug('plot enter {}'.format(type(self).__name__))
        event_seq = self.plot_filters(
            self.seq_filters(),
            event_seq,
            plotter,
        )
        self.__logger.debug('plot exit')

        return event_seq

    @property
    def default_save_name(self):
        """
        
        :return: 
        """
        return self.chart_name

    @property
    def chart_name(self):
        """
        
        :return: 
        """
        return self.mro_save_name

    @property
    def mro_save_name(self):
        """
        
        :return: 
        """
        class_list = type(self).__bases__
        name_list = (
            self.un_camel(cls.__name__) for cls in class_list
        )
        name_list = reversed(list(name_list))
        name = '/'.join(name_list)
        return name

    @staticmethod
    def un_camel(name, delimiter='-'):
        """
        
        :param name: 
        :param delimiter: 
        :return: 
        """
        final = ''
        for item in name:
            if item.isupper():
                final += delimiter + item.lower()
            else:
                final += item
        if final[0] == delimiter:
            final = final[1:]
        return final

    def seq_filters(self):
        """
        
        :return: 
        """
        return ()

    def plot_filters(self, filter_seq, event_seq, plotter, ):

        """

        :param filter_seq:
        :param event_seq:
        :param plotter:
        """

        # filter_seq = tqdm.tqdm(
        #     filter_seq,
        #     desc='filter_event',
        # )

        event_seq, dst_event_seq = itertools.tee(event_seq)
        processed_seq = self.processed_seq(filter_seq, event_seq)

        filter_event = zip(filter_seq, processed_seq)

        # one_line_logger = logging.getLogger('one_line')

        for filter_desc, event_seq in filter_event:

            for event in event_seq:

                # one_line_logger.info('%r\0\r', event.frame.time)

                # one_line_logger.info(
                #     "<<%s>> - %s - [%s] -<%s>\0\r",
                #     filter_desc.name,
                #     event,
                #     event.time,
                #     event.feature
                # )

                filtered = event.feature
                time = 0
                if event.time:
                    time = float(event.time)
                time = time - filter_desc.offset
                plotter.add_point(
                    line_name=filter_desc.name,
                    key=time,
                    value=filtered,
                    plot_options=filter_desc.plot_options
                )

                # one_line_logger.info('\n')
                # one_line_logger.info('%s\n', filter_desc.name)

        self.__logger.debug('chart.reveal() enter')
        plotter.reveal()
        self.__logger.debug('chart.reveal() exit')
        return dst_event_seq

    def processed_seq_legacy(self, filter_seq, event_seq):
        """
        
        :param filter_seq: 
        :param event_seq: 
        :return: 
        """

        def apply_filter_desc(arg):
            """

            :param arg: 
            :return: 
            """
            (fd, es) = arg
            filter_objects = fd.formula.filter_objects_as_list
            es = filter_objects(es)
            return es

        filter_event = self.filter_event(filter_seq, event_seq, )
        filter_event_seq = ((fd, es) for fd, es in filter_event)
        processed_seq = map(apply_filter_desc, filter_event_seq)
        return processed_seq

    def processed_seq_simple(self, filter_seq, event_seq):
        """
        
        :param filter_seq: 
        :param event_seq: 
        :return: 
        """

        filter_event = self.filter_event(filter_seq, event_seq)
        for filter_desc, event_seq in filter_event:
            new_event_seq = self.apply_filter_desc(
                filter_desc,
                event_seq
            )
            yield new_event_seq

    def filter_event(self, filter_seq, event_seq):
        """
        
        :param filter_seq: 
        :param event_seq: 
        :return: 
        """
        event_seq_tuple = self.event_seq_tuple(filter_seq, event_seq)
        filter_event = zip(filter_seq, event_seq_tuple)
        return filter_event

    # noinspection PyMethodMayBeStatic
    def event_seq_tuple(self, filter_seq, event_seq):
        """
        
        :param filter_seq: 
        :param event_seq: 
        :return: 
        """
        filter_count = len(filter_seq)
        event_seq_tuple = itertools.tee(event_seq, filter_count)
        return event_seq_tuple

    @staticmethod
    def apply_filter_desc(filter_desc, event_seq):
        """
        
        :param filter_desc: 
        :param event_seq: 
        :return: 
        """
        filter_objects = filter_desc.formula.filter_objects
        new_event_seq = filter_objects(event_seq)
        return new_event_seq

    def processed_seq_future(self, filter_seq, event_seq):
        """
        
        :param filter_seq: 
        :param event_seq: 
        :return: 
        """

        func_seq = list(
            filter_desc.formula.filter_objects_as_list
            for filter_desc in filter_seq
        )

        func_seq_mapper = FuncSeqMapper(
            caller=self
        )

        processed_seq = func_seq_mapper.map(
            func_seq,
            list(event_seq),
        )

        return processed_seq

    def processed_seq(self, filter_seq, event_seq):
        """
        
        :param filter_seq: 
        :param event_seq: 
        :return: 
        """
        return self.processed_seq_simple(filter_seq, event_seq)
