# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import itertools
import logging
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed

from shot_detector.utils.numerical import shrink
from .base_extractor import BaseExtractor


# noinspection PyAbstractClass
class ParallelExtractor(BaseExtractor):
    """

    It helps only with long videos

    WARNING:
        remember that sending data from process
        to another has its own costs!

    """

    __logger = logging.getLogger(__name__)

    POOL_SIZE = mp.cpu_count()
    IMAGE_GROUP_SIZE = 128

    def transform_frame_images(self, image_seq, **kwargs):
        """
        
        :param image_seq: 
        :param kwargs: 
        :return: 
        """

        future_seq = self.image_group_future_seq(image_seq, **kwargs)
        index_group_seq = self.future_result_seq(future_seq)
        for _, group in sorted(index_group_seq):
            for image in group:
                yield image

    @staticmethod
    def future_result_seq(future_seq):
        """
        
        :param future_seq: 
        :return: 
        """
        future_list = list(future_seq)
        future_seq = as_completed(future_list)
        for future in future_seq:
            yield future.result()

    def image_group_future_seq(self, image_seq, **kwargs):
        """
        
        :param image_seq: 
        :param kwargs: 
        :return: 
        """
        image_group_seq = self.image_group_seq(image_seq)
        with ProcessPoolExecutor(self.POOL_SIZE) as executor:
            for index, image_group in enumerate(image_group_seq):
                # Serialization for submit to ProcessPoolExecutor.
                image_list = list(image_group)
                future = executor.submit(
                    self.local_transform_frame_images,
                    index,
                    image_list,
                    **kwargs
                )
                yield future

    def local_transform_frame_images(self, index, image_list, **kwargs):
        """
        
        :param index: 
        :param image_list: 
        :param kwargs: 
        :return: 
        """
        # Deserialization.
        image_seq = iter(image_list)
        image_seq = super(ParallelExtractor, self) \
            .transform_frame_images(image_seq, **kwargs)
        image_list = list(image_seq)
        return index, image_list

    def image_group_seq(self, image_seq):
        """
        
        :param image_seq: 
        :return: 
        """
        size = self.IMAGE_GROUP_SIZE
        it = iter(image_seq)
        group = list(itertools.islice(it, size))
        while group:
            yield group
            group = list(itertools.islice(it, size))
            # size = random.randint(32, 512)


# Just for experiments and comparison.
def static_format_frame_images(image_seq, **kwargs):
    """
    
    :param image_seq: 
    :param kwargs: 
    :return: 
    """
    image_seq = static_shrink_frame_images(image_seq, **kwargs)
    image_seq = static_normalize_frame_images(image_seq, **kwargs)
    return list(image_seq)


# noinspection PyUnusedLocal
def static_shrink_frame_images(image_seq, width=2, height=2):
    """
    
    :param image_seq: 
    :param width: 
    :param height: 
    :return: 
    """
    for image in image_seq:
        yield shrink(image, 2, 2)


def static_normalize_frame_images(image_seq, colour_dim=3):
    """
    
    :param image_seq: 
    :param colour_dim: 
    :return: 
    """
    for image in image_seq:
        yield image / colour_dim
