# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging


from .base_filter import BaseFilter

class FilterDifference(BaseFilter):

    __logger = logging.getLogger(__name__)

    def reduce_parallel(self, features_list, video_state,  *args, **kwargs):
        if features_list:
            features_res = features_list[0]
            for features in features_list[1:]:
                features_res = features - features_res
            return features_res, video_state
        return features_list, video_state

