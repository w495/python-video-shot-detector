# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import multiprocessing


class QueueWorker(multiprocessing.Process):
    __logger = logging.getLogger(__name__)

    # noinspection PyUnusedLocal
    def __init__(self, task_queue, result_queue, **_kwargs):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        process_name = self.name
        self.__logger.debug('%s: starts' % process_name)
        while True:
            self.__logger.debug('%s: in loop' % process_name)
            next_task = self.task_queue.get()
            self.__logger.debug(
                '%s: get %s ' % (process_name, next_task))
            if next_task is None:
                # Poison pill means shutdown
                self.__logger.debug('%s: exiting' % process_name)
                self.task_queue.task_done()
                self.__logger.debug('%s: break' % process_name)
                break
            self.__logger.debug(
                '%s: call task %s' % (process_name, next_task))
            answer = next_task()
            self.__logger.debug(
                '%s: task %s called' % (process_name, next_task))
            self.task_queue.task_done()
            self.__logger.debug(
                '%s: task %s done' % (process_name, next_task))
            self.result_queue.put(answer)
            self.__logger.debug('%s: answer put' % process_name)

        self.__logger.debug('%s: exit' % process_name)

        return
