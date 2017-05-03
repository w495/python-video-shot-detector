# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import logging

from .sign_change_filter import SignChangeFilter


class AngleChangeFilter(SignChangeFilter):
    """
        Catches change of angle between two feature sequences.
    """

    __logger = logging.getLogger(__name__)

    def filter_features(self, features, use_angle=False, **kwargs):
        prev_sign = 0
        prev_feature = (0, 0)
        for feature in features:
            curr_feature = feature

            curr_sign = int((feature[0] - feature[1]) >= 0)

            diff_feature = 1000 * self.angle(
                (1, curr_feature[0] - prev_feature[0]),
                (1, curr_feature[1] - prev_feature[1])
            )

            result = curr_sign - prev_sign
            if use_angle:
                result = diff_feature * (curr_sign - prev_sign)
            yield feature[0] * 0.0 + result

            prev_sign = curr_sign
            prev_feature = curr_feature
