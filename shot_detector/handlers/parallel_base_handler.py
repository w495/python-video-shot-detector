# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.utils.multiprocessing import SaveStateProcessPool
from .base_handler import BaseHandler


class ParallelBaseHandler(BaseHandler):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    CHUNK_SIZE = 4096

    def handle_video_container(self, video_container, **kwargs):
        """
        
        :param video_container: 
        :param kwargs: 
        :return: 
        """
        process_pool = self.get_process_pool(chunk_size=self.CHUNK_SIZE)
        with process_pool:
            super(ParallelBaseHandler, self).handle_video_container(
                video_container,
                process_pool=process_pool,
                **kwargs)
        return []

    @staticmethod
    def get_process_pool(*args, **kwargs):
        """
        
        :param args: 
        :param kwargs: 
        :return: 
        """
        return SaveStateProcessPool(*args, **kwargs)
