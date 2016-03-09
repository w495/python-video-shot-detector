# -*- coding: utf8 -*-

"""
    The main idea of this module, that you can combine
    any number of any filters without any knowledge about their
    implementation. You have only one requirement — user functions
    should return a filter (or something that can be cast to a filter).
"""

from __future__ import absolute_import, division, print_function

from shot_detector.features.filters import (
    DelayFilter,
    DecisionTreeRegressorSWFilter,
    MinStdRegressionSWFilter
)


WINDOW_SIZE = 25


delay = DelayFilter()

original = delay(0)

dtr = DecisionTreeRegressorSWFilter(
    window_size=25,
    strict_windows=True,
    overlap_size=0,
    #cs=False,
    recursion_limit=1000*20
)

minstd = MinStdRegressionSWFilter(
    window_size=25,
    strict_windows=True,
    overlap_size=0,
    #cs=False,
    recursion_limit=1000*20
)


def multi_dtr(size=25):
    res = min_size_filter_generator(size)
    res = sum(res)/ size
    return res


def min_size_filter_generator(size):
    for offset in xrange(0, size):
        yield delay(offset) | dtr(
            s=size,
            depth=2,
        )