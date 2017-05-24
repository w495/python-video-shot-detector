# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import collections
import os
import os.path

import scipy.misc


def save_feature_image(features, number,
                       subdir='filter',
                       priv='priv',
                       prefix='image',
                       **_):
    """

    cat *.jpg | ffmpeg -f image2pipe  -s 16x16  
        -pix_fmt yuv420p  -_cython:v mjpeg -i - -vcodec libx264 out.mp4


    :param features:
    :param number:
    :param subdir:
    :param priv:
    :param prefix:
    :return:
    """
    path = '%s/%s' % (priv, subdir)
    if isinstance(features, collections.Iterable):
        if not os.path.exists(path):
            os.makedirs(path)
        # noinspection PyTypeChecker
        scipy.misc.imsave(
            '%s/%s-%.10d.jpg' %
            (path, prefix, number),
            features
        )
