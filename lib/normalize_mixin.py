# -*- coding: utf8 -*-

from __future__ import absolute_import


class NormalizeMixin(object):

    def transform_features(self, features, video_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return features, video_state

    def normalize_vector(self, vector):
        rng = vector.max() -  vector.min()
        amin = vector.min()
        return (vector - amin) * 255 / rng

