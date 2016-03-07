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
    SavitzkyGolaySWFilter
)

delay = DelayFilter()

polynomial_approximation = SavitzkyGolaySWFilter(
    strict_windows=True,    # type of window
    window_size=25,         # default size of sliding windows
    overlap_size=0,         # native overlapping of sliding windows
    polyorder=2,            # maximum polynomial order
)


def mole_filter(size=25):
    """
    Returns filter of mean polynomial approximation.

    Simple implementation of mole-algorithm by Sherstobitov A.I.
    and Marchuk V.I. «Method for Separating Trend Using Method
    of Sliding Trend Estimates Multiplication of its Single Source
    Realization and Device for Realization of Said Method.»
    Date of publication: 27.07.2005 Bull. 21
    Invention — RU 2257610 C1

    http://www1.fips.ru/fips_servl/fips_servlet?DB=RUPAT&DocNumber=2257610&TypeFile=html


    :param int size: size of sliding windows
    :return: filter that calculates mean of polynomial approximations.
    """
    res = filter_generator(size)
    res = sum(res)/size
    return res


def filter_generator(size=25):
    """
    Generates the sequence (generator) of filters,

    Each filter compute polynomial approximations for sliding windows
    of the same sizes but starts in different points.
    :param size:
    :return:
    """
    for offset in xrange(size):
        # with delay we try to reconstruct delay of sliding windows
        # to sum it window by window.
        # It is simple but not very effective.
        yield delay(offset) | polynomial_approximation(s=size)
