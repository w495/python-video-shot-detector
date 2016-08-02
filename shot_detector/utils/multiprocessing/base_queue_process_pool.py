# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import Queue
import logging
import multiprocessing
import six
import itertools

from shot_detector.utils.collections import Condenser
from .function_task import FunctionTask
from .queue_worker import QueueWorker


from multiprocessing import Pool

PROCESSES = multiprocessing.cpu_count()
CHUNK_SIZE = 1024
import uuid
import time

#
# Constants representing the state of a pool
#

RUN = 0
CLOSE = 1
TERMINATE = 2

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

    SENTINEL = str(object())


    __logger = multiprocessing.get_logger()

    def __init__(self, processes=PROCESSES, chunk_size=CHUNK_SIZE):
        #multiprocessing.Process.__init__(self)

        self.__logger.setLevel(logging.DEBUG)

        self.chunk_size = chunk_size
        self.processes = processes
        #self.task_queue = multiprocessing.JoinableQueue(chunk_size*2)

        self.task_queue = multiprocessing.Queue()

        self.result_queue = multiprocessing.Queue()

        self.queue_size = 0
        self.value_size = 0
        self.task_counter = 0
        self.worker_list = []

        self.sender_id = None

        self.do_restart = True
        self.result_seq_gist= dict()

        self.worker_handler = multiprocessing.Process(
            target=self._handle_workers
        )
        self.worker_handler.start()




    def _handle_workers(self):
        self._repopulate_pool()
        while True:
            self._repopulate_pool()
            time.sleep(0.1)
            # self.__logger.debug(
            #     'self.worker_list = %s' % self.worker_list
            # )

        return



    # @staticmethod
    # def _handle_workers(pool):
    #     thread = threading.current_thread()
    #
    #     # Keep maintaining workers until the cache gets drained, unless the pool
    #     # is terminated.
    #     while True:
    #         pool._maintain_pool()
    #         time.sleep(0.1)


    # def _maintain_pool(self):
    #     """Clean up any exited workers and start replacements for them.
    #     """
    #     if self._join_exited_workers():
    #         self._repopulate_pool()


    # def _join_exited_workers(self):
    #     """Cleanup after any worker processes which have exited due to reaching
    #     their specified lifetime.  Returns True if any workers were cleaned up.
    #     """
    #     cleaned = True
    #     for i in reversed(range(len(self.worker_list))):
    #         worker = self.worker_list[i]
    #         #print ("worker =", worker, len(self.worker_list))
    #         if worker.exitcode is not None:
    #             #print ("worker =", worker, worker.exitcode)
    #             # worker exited
    #             worker.join()
    #             cleaned = True
    #             del self.worker_list[i]
    #     return cleaned

    def _repopulate_pool(self):
        """Bring the number of pool processes up to the specified number,
        for use after reaping workers which have exited.
        """

        # if self.do_restart:
        #     self.task_queue \
        #         = multiprocessing.JoinableQueue(self.chunk_size)
        #     self.result_queue = multiprocessing.Queue()
        #     self.do_restart = False

        for worker_number in range(self.processes - len(self.worker_list)):
            queue_worker = QueueWorker(
                task_queue=self.task_queue,
                result_queue=self.result_queue,
                worker_number=worker_number,
                sender_id = self.sender_id
            )
            self.worker_list.append(queue_worker)
            queue_worker.daemon = True
            queue_worker.start()



    def __enter__(self):
        self.do_restart = False
        self.sender_id = str(uuid.uuid4())
        self.result_seq_gist[self.sender_id] = list()


        self.__logger.info('self.sender_id = %s' % self.sender_id)

        return self

    # noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
    def __exit__(self, type_, _value, _traceback):
        # for _ in self.worker_list:
        #     self.task_queue.put(QueueWorker.SENTINEL)
            #self.worker_list = list()

        # for worker in self.worker_list:
        #     worker.join()
        self.do_restart = True

        self.__logger.info('done %s' % self.worker_list)


        #self.join()
        #self.close()

    #
    # def close(self):
    #     self.__logger.info('self.queue_size _ = %s' % self.queue_size)
    #     for _ in self.worker_list:
    #         self.task_queue.put(QueueWorker.SENTINEL)
    #     self.worker_list = list()


    def put_task(self, func,  *args, **kwargs):
        self.task_counter += 1
        handle_task_func = self.handle_task

        task_id = "{self_id}-{task_id:0>16}".format(
            self_id=self.sender_id,
            task_id=self.task_counter
        )
        task = FunctionTask(
            self.sender_id,
            task_id,
            handle_task_func,
            func,
            *args,
            **kwargs
        )
        self._put_task(task)


    @staticmethod
    def handle_task(func, *args, **kwargs):
        result = func(*args, **kwargs)
        return result

    @staticmethod
    def handle_task__(func,
            iterable,
            __queue_number=None,
            reduce_func=list,
            *args,
            **kwargs):
        result = (func(item, *args, **kwargs) for item in iterable)
        result = reduce_func(result)
        return __queue_number, result

    def _put_task(self, task):
        self.queue_size += 1
        self.task_queue.put(task)
        self.task_queue.put(QueueWorker.SENTINEL)

        return self.queue_size

    def get_result(self, block=True, timeout=None):
        return self.result_queue.get(block, timeout)





    # noinspection PyUnusedLocal
    def join(self, block=True, timeout=None, reduce_func=list, **_kwargs):
        """

        :param block:
        :param timeout:
        :param reduce_func:
        :param _kwargs:
        :return:
        """
        self.__logger.info('self.queue_size 1 = %s' % self.task_queue.qsize())
        self.__logger.info('self.queue_size 1 = %s' % self.worker_list)


        for worker in self.worker_list:
            worker.join()


            #self.worker_list = list()

        # #self.task_queue.join()
        self.result_queue.put(self.SENTINEL)


        self.__logger.info('self.queue_size 2 = %s' % self.task_queue.qsize())
        results = self.get_all_results(block, timeout, reduce_func)
        self.__logger.info('self.queue_size 4 = %s' % self.task_queue.qsize())

        # for _ in self.worker_list:
        #     self.task_queue.put(QueueWorker.SENTINEL)
        return results

    # noinspection PyUnusedLocal
    def get_all_results(self, block=True, timeout=None, reduce_func=list, **_kwargs):
        """

        :param block:
        :param timeout:
        :param reduce_func:
        :param _kwargs:
        :return:
        """
        self.__logger.info('self.queue_size 3 = %s' % [self.queue_size, self.value_size, self.result_queue.empty()])


        result_seq = (
            result for result in iter(
                self.result_queue.get,
                self.SENTINEL
            )
        )


        result_seq = sorted(result_seq,
            key=lambda item: item.task_id,
        )


        tmp_result_seq_gist =  {
            k:list(g) for k, g in itertools.groupby(
                result_seq,
                key=lambda item: item.sender_id,
            )
        }


        for key, val_list in six.iteritems(tmp_result_seq_gist):
            self.result_seq_gist.setdefault(key, []).extend(val_list)


        result_seq = self.result_seq_gist[self.sender_id]

        result_seq = (item.result for item in result_seq)

        self.__logger.info('self.queue_size 3.1 = %s' % [self.queue_size, self.value_size])

        result_seq = reduce_func(result_seq)
        self.__logger.info('self.queue_size 3.2 = %s' % [
            self.queue_size, self.value_size])

        self.queue_size = 0
        self.value_size = 0

        return result_seq
