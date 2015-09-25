# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from collections import OrderedDict
import logging
import multiprocessing
import time
import dill
import six

from shot_detector.objects import SmartDict

from .base_point_handler import BasePointHandler



class QueueWorker(multiprocessing.Process):
    __logger = logging.getLogger(__name__)

    def __init__(self, task_queue, result_queue):
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



class FunctionTask(object):
    """
    Тask that call fnction

    """

    __logger = logging.getLogger(__name__)

    def __init__(self, func, *args, **kwargs):
        """
        Creates FunctionTask object.
        Pack triple `(func, *args, **kwargs)` into dill-dumped object
        to send it to another process.

        :param func: function or method
            function, that you want to execute like  func(*args, **kwargs).
        :param args:
            positional arguments of function `func`.
        :param kwargs:
            named arguments of function `func`.
        """

        self.dumped_data = dill.dumps(dict(
            func=func,
            args=args,
            kwargs=kwargs,
        ))
        self.result = None

    def __call__(self):
        """
        Unpack dill-dumped object into triple `(func, *args, **kwargs)`
        and execute `func(*args, **kwargs)`

        :return: any
            result of func(*args, **kwargs).
        """
        dumped_dict = dill.loads(self.dumped_data)
        obj = SmartDict(dumped_dict)
        self.result = obj.func(*obj.args, **obj.kwargs)
        return self.result


class Condenser(object):

    MAXLEN = 1024

    def __init__(self, maxlen=MAXLEN):
        self._is_charged = False
        self.maxlen = maxlen
        self.list = []

    def charge(self, value):
        if self._is_charged:
            self.list = []
        self._is_charged = False
        self.list += [value]
        if len(self.list) == self.maxlen:
            self._is_charged = True
        return self._is_charged

    @property
    def is_charged(self):
        return self._is_charged

    def get(self):
        if self.is_charged:
            return self.list
        return []


class BaseQueueProcessPool(object):

    __logger = logging.getLogger(__name__)

    def __init__(self, processes=4, buffer_size = 1024):
        self.processes = processes
        self.tasks_queue = multiprocessing.JoinableQueue()
        self.result_queue = multiprocessing.Queue()
        self.queue_size = 0
        self.value_size = 0

        self.worker_list = OrderedDict(
            [
                (worker_number, QueueWorker(self.tasks_queue, self.result_queue))
                for worker_number in xrange(self.processes)
            ]
        )
        self.condenser = Condenser(buffer_size)


    def start(self):
        for worker_number, worker in six.iteritems(self.worker_list):
            worker.start()

    def apply_async(self, func, value, *args, **kwargs):
        self.value_size += 1
        self.condenser.charge(value)
        if self.condenser.is_charged:
            values = self.condenser.get()
            self.map_async(func, values, *args, **kwargs)

    def map_async(self, func, iterable, map_func=None, *args, **kwargs):
        if not map_func:
            map_func = self.map
        task = FunctionTask(
            map_func, func, iterable, *args, **kwargs
        )
        self.put_task(task)

    @staticmethod
    def map(func, iterable, reduce_func=list, *args, **kwargs):
        result = (func(item, *args, **kwargs) for item in iterable)
        result = reduce_func(result)
        return result

    def put_task(self, task):
        self.queue_size += 1
        return self.tasks_queue.put(task)

    def get_result(self, block=True, timeout=None):
        return self.result_queue.get(block, timeout)

    def close(self):
        self.__logger.info('self.queue_size = %s' % self.processes)
        for i in xrange(self.processes):
            self.tasks_queue.put(None)

    def join(self, block=True, timeout=None, reduce_func=list):
        self.__logger.info('self.queue_size 1 = %s' % self.tasks_queue.qsize())
        self.tasks_queue.join()
        self.__logger.info('self.queue_size 2 = %s' % [self.queue_size, self.value_size])
        result = (self.get_result(block, timeout) for i in xrange(self.queue_size))
        result = reduce_func(result)
        return result

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.close()
        self.join()


class SaveStateProcessPool(BaseQueueProcessPool):
    @staticmethod
    def map(func, iterable, *args, **kwargs):
        result = None
        for item in iterable:
            result = func(item, prev_result=result, *args, **kwargs)
        return result


class ParallelHandler(BasePointHandler):
    __logger = logging.getLogger(__name__)

    def handle_video_container(self, video_container, video_state=None, *args, **kwargs):

        with SaveStateProcessPool(64) as queue_pool:
            super(ParallelHandler, self).handle_video_container(
                video_container,
                video_state,
                queue_pool=queue_pool,
                *args, **kwargs)

        return video_state

    def handle_selected_frame(self, frame, video_state = None, queue_pool=None, *args, **kwargs):

        queue_pool.apply_async(
            func = self.handle_sequential_buffer,
            value = frame,
            video_state = video_state,
            *args, **kwargs
        )

        return video_state

    def handle_sequential_buffer(self, frame, video_state=None, prev_result=None, *args, **kwargs):
        if prev_result:
            video_state = prev_result

        video_state = super(ParallelHandler, self).handle_selected_frame(
            frame,
            video_state,
            *args, **kwargs
        )
        return video_state
