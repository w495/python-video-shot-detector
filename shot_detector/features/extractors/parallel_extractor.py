# -*- coding: utf8 -*-

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

    WARNINIG:
        remember that sending data from process
        to another has its own costs!

    """

    __logger = logging.getLogger(__name__)

    POOL_SIZE = mp.cpu_count()
    IMAGE_GROUP_SIZE = 128

    def transform_frame_images(self, image_seq, **kwargs):

        future_seq = self.image_group_future_seq(image_seq, **kwargs)
        index_group_seq = self.future_result_seq(future_seq)
        for _, group in sorted(index_group_seq):
            for image in group:
                yield image

    def future_result_seq(self, future_seq):
        future_list = list(future_seq)
        future_seq = as_completed(future_list)
        for future in future_seq:
            yield future.result()

    def image_group_future_seq(self, image_seq, **kwargs):
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
        # Deserialization.
        image_seq = iter(image_list)
        image_seq = super(ParallelExtractor, self) \
            .transform_frame_images(image_seq, **kwargs)
        image_list = list(image_seq)
        return index, image_list

    def image_group_seq(self, image_seq):
        size = self.IMAGE_GROUP_SIZE
        it = iter(image_seq)
        group = list(itertools.islice(it, size))
        while group:
            yield group
            group = list(itertools.islice(it, size))
            # size = random.randint(32, 512)


# Just for experiments and comparison.
def static_format_frame_images(image_seq, **kwargs):
    image_seq = static_shrink_frame_images(image_seq, **kwargs)
    image_seq = static_normalize_frame_images(image_seq, **kwargs)
    return list(image_seq)


def static_shrink_frame_images(image_seq, width=2, height=2):
    for image in image_seq:
        yield shrink(image * 1.0, 2, 2)


def static_normalize_frame_images(image_seq, colour_dim=3):
    for image in image_seq:
        yield image / colour_dim
