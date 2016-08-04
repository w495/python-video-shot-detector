# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import multiprocessing
from multiprocessing import Queue

from shot_detector.utils.collections import Condenser
from .function_task import FunctionTask
from .queue_worker import QueueWorker

PROCESSES = multiprocessing.cpu_count()
CHUNK_SIZE = 1024


class BaseQueueProcessPool(object):
    """
        π — process
        φ — function
        φ(·) — call of function φ
        ν(·) — value of φ(·)

        {
            {φ,A}, {φ,B}, {φ,C},
            {φ,D}, {φ,E}, {φ,F},
            ...,
            {φ,X}, {φ,Y}, {φ,Z}.
        }
        =>
            {φ, A, B, C },
            {φ, D, E, F },
                ... ,
            {φ, X, Y, Z }.
        =>
            π₁ {φ, A, B, C };
            π₂ {φ, D, E, F };
                π   ... ;
            πₙ {φ, X, Y, Z }.
        =>
            π₁ {φ(A), φ(B), φ(C)};
            π₂ {φ(D), φ(E), φ(F)};
                π   ... ;
            πₙ {φ(X), φ(Y), φ(Z)}.
        =>
            π₁ {ν(A), ν(B), ν(C)};
            π₂ {ν(D), ν(E), ν(F)};
                π   ... ;
            πₙ {ν(X), ν(Y), ν(Z)}.
        =>
            [
                {ν(A), ν(B}, ν(C)},
                {ν(D), ν(E}, ν(F)},
                    ...
                {ν(X), ν(Y), ν(Z)}.
            ]
        =>
        [
            ν(A), ν(B}, ν(C),
            ν(D), ν(E}, ν(F),
                ...
            ν(X), ν(Y), ν(Z)
        ]


    """

    __logger = logging.getLogger(__name__)

    def __init__(self, processes=PROCESSES, chunk_size=CHUNK_SIZE):
        self.processes = processes
        self.task_queue = multiprocessing.JoinableQueue(chunk_size * 2)
        self.result_queue = multiprocessing.Queue()
        self.condenser = Condenser(chunk_size)
        self.queue_size = 0
        self.value_size = 0
        self.worker_list = [
            QueueWorker(
                task_queue=self.task_queue,
                result_queue=self.result_queue,
                worker_number=worker_number
            )
            for worker_number in range(self.processes)
            ]

    def __enter__(self):
        self.start()
        return self

    # noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
    def __exit__(self, type_, _value, _traceback):
        self.join()
        self.close()

    def start(self):
        for worker in self.worker_list:
            worker.start()

    def apply_partial(self, func, value, *args, **kwargs):
        is_bulk_applied = self.apply_async(func, value, *args, **kwargs)
        if is_bulk_applied:
            try:
                result = self.get_all_results(block=False, *args,
                                              **kwargs)
            except Queue.Empty:
                result = []
            return result
        return []

    def apply_async(self, func, value, *args, **kwargs):
        self.value_size += 1
        self.condenser.charge(value)
        if self.condenser.is_charged:
            values = self.condenser.get()
            self.map_async(func, values, *args, **kwargs)
            return True
        return False

    def map_async(self, func, iterable, map_func=None, *args, **kwargs):
        if not map_func:
            map_func = self.map
        task = FunctionTask(
            map_func, func, iterable, self.queue_size, *args, **kwargs
        )
        self.put_task(task)

    @staticmethod
    def map(func, iterable, reduce_func=list, __queue_number=None,
            *args, **kwargs):
        result = (func(item, *args, **kwargs) for item in iterable)
        result = reduce_func(result)
        return __queue_number, result

    def put_task(self, task):
        self.queue_size += 1
        self.task_queue.put(task)
        return self.queue_size

    def get_result(self, block=True, timeout=None):
        return self.result_queue.get(block, timeout)

    def close(self):
        """

        """
        self.__logger.info('self.queue_size = %s' % self.processes)
        for i in range(self.processes):
            self.task_queue.put(None)

    # noinspection PyUnusedLocal
    def join(self, block=True, timeout=None, reduce_func=list,
             **_kwargs):
        """

        :param block:
        :param timeout:
        :param reduce_func:
        :param _kwargs:
        :return:
        """
        self.__logger.info(
            'self.queue_size 1 = %s' % self.task_queue.qsize())
        self.task_queue.join()
        self.__logger.info(
            'self.queue_size 2 = %s' % self.task_queue.qsize())
        results = self.get_all_results(block, timeout, reduce_func)
        self.__logger.info(
            'self.queue_size 4 = %s' % self.task_queue.qsize())
        return results

    # noinspection PyUnusedLocal
    def get_all_results(self, block=True, timeout=None,
                        reduce_func=list, **_kwargs):
        """

        :param block:
        :param timeout:
        :param reduce_func:
        :param _kwargs:
        :return:
        """
        self.__logger.info('self.queue_size 3 = %s' % [self.queue_size,
                                                       self.value_size,
                                                       self.result_queue.empty()])
        result = sorted(self.get_result(block, timeout) for _ in
                        xrange(self.queue_size))
        self.__logger.info(
            'self.queue_size 3.1 = %s' % [self.queue_size,
                                          self.value_size])
        result = reduce_func(result)
        return result
