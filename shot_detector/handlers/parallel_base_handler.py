# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.utils.multiprocessing import SaveStateProcessPool
from .base_handler import BaseHandler


class ParallelBaseHandler(BaseHandler):
    __logger = logging.getLogger(__name__)

    CHUNK_SIZE = 4096

    def handle_video_container(self, video_container, **kwargs):
        with self.get_process_pool(
            chunk_size=self.CHUNK_SIZE) as process_pool:
            super(ParallelBaseHandler, self).handle_video_container(
                video_container,
                process_pool=process_pool,
                **kwargs)
        return []

    @staticmethod
    def get_process_pool(*args, **kwargs):
        return SaveStateProcessPool(*args, **kwargs)
