# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import multiprocessing
import logging


class QueueWorker(multiprocessing.Process):

    __logger = logging.getLogger(__name__)

    def __init__(self, task_queue, result_queue, *args, **kwargs):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        self.__logger.debug('%s: starts' % proc_name)
        while True:
            self.__logger.debug('%s: in loop' % proc_name)
            next_task = self.task_queue.get()
            self.__logger.debug('%s: get %s ' % (proc_name, next_task))
            if next_task is None:
                # Poison pill means shutdown
                self.__logger.debug('%s: exiting' % proc_name)
                self.task_queue.task_done()
                self.__logger.debug('%s: break' % proc_name)
                break
            self.__logger.debug('%s: call task %s' % (proc_name, next_task))
            answer = next_task()
            self.__logger.debug('%s: task %s called' % (proc_name, next_task))
            self.task_queue.task_done()
            self.__logger.debug('%s: task %s done' % (proc_name, next_task))
            self.result_queue.put(answer)
            self.__logger.debug('%s: answer put' % (proc_name))

        self.__logger.debug('%s: exit' % proc_name)

        return


