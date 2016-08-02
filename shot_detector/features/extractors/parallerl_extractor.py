# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import collections
import itertools
from multiprocessing import cpu_count, Pool

from .base_extractor import BaseExtractor


def run_sync_frame_image_features(arg,):
    (extractor, image_seq, kwargs) = arg
    return extractor.sync_frame_image_features(image_seq, **kwargs)


# noinspection PyAbstractClass
class ParallelExtractor(BaseExtractor):

    POOL_SIZE = cpu_count()
    IMAGE_GROUP_SIZE = 16
    IMAGE_GROUP_SEQ_SLICE_SIZE = 1024

    def frame_features(self, frame_seq, **kwargs):
        """

        :type frame_seq: collections.Iterable
        :param frame_seq:
        :param kwargs:
        :return:
        """
        assert isinstance(frame_seq, collections.Iterable)
        av_frames = self.av_frames(frame_seq, **kwargs)
        formatted_av_frames = self.format_av_frames(av_frames, **kwargs)
        frame_images = self.frame_images(formatted_av_frames, **kwargs)
        features = self.__async_image_features(frame_images, **kwargs)
        return features

    def __async_image_features(self, image_seq, **kwargs):
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
                async_result = pool.put_task(run_sync_frame_image_features, group_list)
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
        return itertools.izip_longest(fillvalue=fillvalue, *args)
