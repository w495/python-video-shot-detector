# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

from collections import OrderedDict
#
# from multiprocessing.dummy import Pool

import multiprocessing

import time

from av.video.frame import VideoFrame

from shot_detector.objects import SmartDict, BaseVideoState

from .base_handler import BaseHandler




from .base_point_handler  import BasePointHandler



class ParallelBuffer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        print('Start: %s' % proc_name)
        while True:
            print('Start: %s 1' % proc_name)

            next_task = self.task_queue.get()
            print('next_task = ', next_task)

            if next_task is None:
                # Poison pill means shutdown
                print('%s: Exiting' % proc_name)
                self.task_queue.task_done()
                print('%s: break' % proc_name)
                break
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        print('%s: exit' % proc_name)
        return


class Task(object):
    def __init__(self, obj, buffer, video_state, args, kwargs):
        self.obj = obj
        self.buffer = buffer

        self.video_state = video_state
        self.args = args
        self.kwargs = kwargs
        self.result = None

    def __call__(self):
        print('__CA__')
        handler = self.obj
        func = handler.handle_sequential_buffer
        self.result = func(self.buffer, self.video_state, *self.args, **self.kwargs)
          # pretend to take some time to do the work
        return self.result

    def __str__(self):
        return '%s' % self.result




class ParallelHandler(BasePointHandler):

    __logger = logging.getLogger(__name__)


    def handle_video_container(self, video_container, video_state=None, *args, **kwargs):

        size = 10

        tasks_queue = multiprocessing.JoinableQueue()
        result_queue = multiprocessing.Queue()
        buffer_list = OrderedDict([(i, ParallelBuffer(tasks_queue, result_queue)) for i in xrange(size)])

        for n, buffer in six.iteritems(buffer_list):
            buffer.start()

        parallel_state = SmartDict(
            pool_size=size,
            buffer=SmartDict(
                list = [],
                max_size=1500,
                size = 0,
                number=0,
            ),
            tasks_queue=tasks_queue,
            result_queue=result_queue,
        )

        super(ParallelHandler, self).handle_video_container(
            video_container=video_container,
            video_state=video_state,
            parallel_state = parallel_state,
            *args, **kwargs)

        for i in xrange(parallel_state.pool_size):
            parallel_state.tasks_queue.put(None)
        for i in xrange(parallel_state.buffer.number):
            parallel_state.result_queue.get()
        return video_state




    def handle_selected_frame(self, frame, video_state=None, parallel_state = None, *args, **kwargs):

        parallel_state.buffer.list  += [frame]
        parallel_state.buffer.size = parallel_state.buffer.size + 1
        if parallel_state.buffer.size == parallel_state.buffer.max_size:
            video_state = self.handle_parallel_buffer(
                buffer_list=parallel_state.buffer.list,
                video_state=video_state,
                parallel_state = parallel_state,
                *args, **kwargs
            )

            parallel_state.buffer.list = []
            parallel_state.buffer.number += 1
            parallel_state.buffer.size = 0

            print ('parallel_state.buffer.number = ', parallel_state.buffer.number)

        return video_state


    def handle_parallel_buffer(self, buffer_list, video_state=None, parallel_state=None, *args, **kwargs):
        parallel_state.tasks_queue.put(
            Task(
                self,
                buffer_list,
                video_state,
                args,
                kwargs
            )
        )
        return video_state

    def handle_sequential_buffer(self, sequential_buffer, video_state=None, *args, **kwargs):
        for frame in sequential_buffer:
            video_state = super(ParallelHandler, self).handle_selected_frame(
                frame=frame,
                video_state=video_state,
                *args, **kwargs
            )
        return video_state

