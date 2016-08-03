# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import collections
import ctypes, itertools
import multiprocessing
import multiprocessing as mp
from multiprocessing import cpu_count, Pool, Process

from concurrent.futures import ProcessPoolExecutor
from .base_extractor import BaseExtractor


from queue import Queue
from threading import Thread
import numpy as np

from .vector_based import VectorBased
_size = 256
# создание массива комплексных чисел размерностью 3х3х3
arr = np.random.rand(_size, _size, _size) \
       + np.random.rand(_size, _size, _size) * 1j


# число потоков
nwork = 4


def __group_seq(iterable, n, fillvalue=None):
    """
        Collect data into fixed-length chunks or blocks
        __group_seq([1,2,3,4,5,6,7], 3, 0) --> (1,2,3) (4,5,6) (7,0,0)
    """
    args = [iter(iterable)] * n
    return itertools.zip_longest(fillvalue=fillvalue, *args)


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.zip_longest(fillvalue=fillvalue, *args)


def run_sync_frame_image_features(arg,):
    (extractor, image_seq, kwargs) = arg
    return extractor.sync_frame_image_features(image_seq, **kwargs)



# noinspection PyAbstractClass
class ParallelExtractor(VectorBased):

    POOL_SIZE = cpu_count()
    IMAGE_GROUP_SIZE = 1024
    IMAGE_GROUP_SEQ_SLICE_SIZE = 1024

    def frame_features(self, frame_seq, **kwargs):
        """

        :type frame_seq: collections.Iterable
        :param frame_seq:
        :param kwargs:
        :return:
        """
        assert isinstance(frame_seq, collections.Iterable)
        frame_seq = self.av_frames(frame_seq, **kwargs)
        frame_seq = self.format_av_frames(frame_seq, **kwargs)
        image_seq = self.frame_images(frame_seq, **kwargs)
        image_seq = self.__format_frame_images(image_seq, **kwargs)
        feature_seq = self.frame_image_features(image_seq, **kwargs)
        return feature_seq



    def __format_frame_images(self, image_seq, **kwargs):


        image_seq, image_seq2 = itertools.tee(image_seq)

        image_group_seq = self.__group_seq(image_seq, self.IMAGE_GROUP_SIZE)


        for group in image_group_seq:
            list(group)
            print('group')
            yield group

        #
        # return self.format_frame_images(image_seq2, **kwargs)




    def __async_image_features__(self, image_seq, **kwargs):
        """

        :param image_seq:
        :param kwargs:
        :return:
        """
        image_group_seq = self.__group_seq(image_seq, self.IMAGE_GROUP_SIZE)
        async_group_seq = self.__async_feature_groups(image_group_seq, **kwargs)
        for async_group in async_group_seq:
            feature_seq = async_group.get()
            for feature in feature_seq:
                yield feature

    def __async_feature_groups(self, image_group_seq, **kwargs):
        """

        :param image_group_seq:
        :return:
        """
        pool = Pool(processes=self.POOL_SIZE)
        group_seq = self.__add_self(image_group_seq, **kwargs)
        while True:
            group_islice = itertools.islice(group_seq, self.IMAGE_GROUP_SEQ_SLICE_SIZE)
            group_list = list(group_islice)
            if group_list:
                async_result = pool.map_async(run_sync_frame_image_features,
                                      group_list)
                yield async_result
            else:
                break

    def __add_self(self, islice, **kwargs):
        for item in islice:
            yield (self, item, kwargs)

    def sync_frame_image_features(self, image_seq, **kwargs):
        for image in image_seq:
            if image is None:
                return []
        image_seq = self.format_frame_images(image_seq, **kwargs)
        features = self.frame_image_features(image_seq, **kwargs)
        return list(features)

    @staticmethod
    def __group_seq(iterable, n, fillvalue=None):
        """
            Collect data into fixed-length chunks or blocks
            __group_seq([1,2,3,4,5,6,7], 3, 0) --> (1,2,3) (4,5,6) (7,0,0)
        """
        args = [iter(iterable)] * n
        return itertools.zip_longest(fillvalue=fillvalue, *args)
