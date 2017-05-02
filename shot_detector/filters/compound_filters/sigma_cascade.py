# -*- coding: utf8 -*-

"""
    The main idea of this module, that you can combine
    any number of any filters without any knowledge about their
    implementation. You have only one requirement — user functions
    should return a filter (or something that can be cast to a filter).
"""

from __future__ import absolute_import, division, print_function

from shot_detector.filters import (
    DelayFilter,
    MeanSWFilter,
    StdSWFilter,
)

WINDOW_SIZE = 25

delay = DelayFilter()

original = delay(0)

mean = MeanSWFilter(
    # window_size=50,
    # strict_windows=True,
    # mean_name='EWMA',
    cs=False,
)

std = StdSWFilter(
    window_size=25,
    strict_windows=True,
    cs=False,
)


def multi_bill(start=5, stop=50, step=None, pivot=None, **kwargs):
    if step is None:
        step = 1
    res = min_size_filter_generator(start, stop, step, pivot, **kwargs)
    res = sum(res) / (stop - start) / step
    return res


def min_size_filter_generator(start, stop, step=None, sigma=None,
                              **kwargs):
    if step is None:
        step = 1
    if sigma is None:
        sigma = 3
    for csize in xrange(start, stop, step):
        cmean = mean(s=csize, **kwargs)
        cstd = std(s=csize, **kwargs)
        bill = (original > (cmean + sigma * cstd)) | int
        yield bill
