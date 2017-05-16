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

from shot_detector.charts import Plotter
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

    def plot_events(self, event_seq, service_options=None, **_):
        """
        
        :param event_seq: 
        :param service_options: 
        :return: 
        """

        event_seq = self.limit_seq(
            event_seq,
            first=service_options.get('first_frame', 0),
            last=service_options.get('last_frame', 60),
            as_stream=service_options.get('as_stream', False)
        )

        default_save_name = self.default_save_name()
        plot_save_name = service_options.get(
            'plot_save_name',
            default_save_name
        )
        if not plot_save_name:
            plot_save_name = default_save_name

        print('service_options = ', service_options)
        plotter = Plotter(
            xlabel=service_options.get('plot_xlabel'),
            ylabel=service_options.get('plot_ylabel'),
            width=service_options.get('plot_width'),
            height=service_options.get('plot_height'),
            font_family=service_options.get('plot_font_family'),
            font_size=service_options.get('plot_font_size'),
            save_dir=service_options.get('plot_save_dir'),
            save_format=service_options.get('plot_save_format'),
            save_name=plot_save_name,
        )

        self.__logger.debug('plot enter {}'.format(type(self).__name__))
        event_seq = self.plot_filters(
            self.seq_filters(),
            event_seq,
            plotter,
        )
        self.__logger.debug('plot exit')

        return event_seq

    def default_save_name(self):
        class_list = type(self).__bases__
        name_list = (
            self.un_camel(cls.__name__) for cls in class_list
        )
        name = '--'.join(name_list)
        return name

    @staticmethod
    def un_camel(name, delim='-'):
        final = ''
        for item in name:
            if item.isupper():
                final += delim + item.lower()
            else:
                final += item
        if final[0] == delim:
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
        event_seq, dst_event_seq = itertools.tee(event_seq)
        processed_seq = self.processed_seq(filter_seq, event_seq)

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
                time = time - filter_desc.offset
                plotter.add_point(
                    line_name=filter_desc.name,
                    key=time,
                    value=filtered,
                    plot_options=filter_desc.plot_options
                )

        self.__logger.debug('chart.reveal() enter')
        plotter.reveal(
            display_mode={
                plotter.Mode.SAVE_PLOT,
                plotter.Mode.SHOW_PLOT
            },
        )
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
