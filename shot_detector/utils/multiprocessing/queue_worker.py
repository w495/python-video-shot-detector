# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import multiprocessing
from multiprocessing import current_process


class QueueWorker(multiprocessing.Process):

    __logger = multiprocessing.get_logger()

    SENTINEL = str(object())


    # noinspection PyUnusedLocal
    def __init__(self,
                 task_queue,
                 result_queue,
                 worker_number,
                 sender_id,
                 **_kwargs):
        multiprocessing.Process.__init__(self)
        self.__logger.setLevel(logging.DEBUG)

        self.task_queue = task_queue
        self.result_queue = result_queue
        self.worker_number = worker_number
        self.sender_id = sender_id


    # noinspection PyUnusedLocal
    def re_init(self, task_queue, result_queue):
        self.task_queue = task_queue
        self.result_queue = result_queue


    def run__(self):
        process_name = "{}-{}".format(self.name, self.worker_number)
        self.__logger.debug('%s: starts' % process_name)
        try:
            for task in iter(self.task_queue.get, self.SENTINEL):
                self.__logger.debug('%s: in loop' % process_name)
                answer = task()
                self.task_queue.task_done()
                self.result_queue.put(answer)
        except Exception, e:
             self.result_queue.put("%s failed with: %s" % (current_process().name, e.message))
        return True


    def run(self):
        process_name = "{}-{}-{}".format(self.sender_id, self.name,
                                      self.worker_number)
        self.__logger.debug('%s: starts' % process_name)
        while True:
            self.__logger.debug('%s: in loop' % process_name)
            next_task = self.task_queue.get()
            self.__logger.debug('%s: get %s ' % (process_name, next_task))
            if next_task == self.SENTINEL:
                # Poison pill means shutdown
                self.__logger.debug('%s: exiting' % process_name)
                #self.task_queue.task_done()
                self.__logger.debug('%s: break' % process_name)
                break

            self.__logger.debug('%s: call task %s' % (
                process_name, next_task))

            self.__logger.debug('%s: call task %s' % (
                process_name, next_task.sender_id))

            answer = next_task()

            sender_id = answer.sender_id
            self.__logger.debug('%s: task %s called' % (process_name, next_task))
            #self.task_queue.task_done()
            self.__logger.debug('%s: task %s done' % (process_name, self.result_queue))
            self.result_queue.put(answer)
            self.__logger.debug('%s: answer put' % process_name)

        self.__logger.debug('%s: exit' % process_name)

        return


