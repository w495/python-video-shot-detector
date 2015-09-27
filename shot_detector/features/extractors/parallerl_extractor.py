# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from multiprocessing import Pool

from shot_detector.utils.collections import Condenser
from shot_detector.utils.multiprocessing import pack_function_for_map

from .base_extractor import BaseExtractor



class ParallelExtractor(BaseExtractor):

    __condenser = Condenser(16)
    __extractor_pool_size = 8

    def extract_frame_features(self, frame, video_state, *args, **kwargs):
        image, video_state = self.build_image(frame, video_state)
        features, video_state = self.handle_image(image, video_state, *args, **kwargs)
        return features, video_state

    def handle_image(self, image, video_state, extractor_pool=None, *args, **kwargs):
        extractor_pool = video_state.get('extractor_pool', None)
        if not extractor_pool:
            extractor_pool = Pool(self.__extractor_pool_size)
        else:
            video_state.extractor_pool = None
        self.__condenser.charge(image)
        features = []
        if self.__condenser.is_charged:
            images = self.__condenser.get()
            features_video_state= extractor_pool.map(
                *pack_function_for_map(
                    super(ParallelExtractor, self).handle_image,
                    images,
                    video_state
                )
            )
            for _features, _ in features_video_state:
                features += [_features]
            _, _vstate = features_video_state[-1]
            video_state = _vstate

        video_state.extractor_pool =  extractor_pool
        return features, video_state
