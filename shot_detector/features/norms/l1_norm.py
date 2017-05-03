# -*- coding: utf8 -*-


from __future__ import absolute_import, division, print_function

import numpy as np

from .base_norm import BaseNorm


class L1Norm(BaseNorm):
    @classmethod
    def length(cls, vector, use_abs=False, **kwargs):
        """
            FFMPEG-like method
            http://www.luckydinosaur.com/u/ffmpeg-scene-change-detector
            l1-norm, Also called «Manhattan norm», Also called «SAD»
            :param vector:
            :param use_abs:
        """

        if not hasattr(vector, 'size'):
            return vector

        diff_vector = vector
        if use_abs:
            diff_vector = np.abs(vector)
        sad = np.sum(diff_vector)
        mean_sad = 1.0 * sad / vector.size
        return mean_sad
