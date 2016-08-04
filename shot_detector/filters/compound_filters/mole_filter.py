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
    SavitzkyGolaySWFilter
)

WINDOW_SIZE = 25

POLYORDER = 2

delay = DelayFilter()

original = delay(0)

same_size_polynomial_approximation = SavitzkyGolaySWFilter(
    strict_windows=True,  # all windows with the same size
    overlap_size=0,  # native overlapping of sliding windows
    window_size=WINDOW_SIZE,  # default size of sliding windows
    polyorder=POLYORDER,  # maximum polynomial order
)

polynomial_approximation = SavitzkyGolaySWFilter(
    strict_windows=False,  # windows with real size ∈ [0, window_size]
    overlap_size=0,  # native overlapping of sliding windows
    window_size=WINDOW_SIZE,  # default size of sliding windows
    polyorder=POLYORDER,  # maximum polynomial order
)


def mole_filter(size=25):
    """
    Returns advanced filter of mean polynomial approximation.

    Advanced implementation of mole-algorithm by Sherstobitov A.I.
    and Marchuk V.I. «Method for Separating Trend Using Method
    of Sliding Trend Estimates Multiplication of its Single Source
    Realization and Device for Realization of Said Method.»
    Date of publication: 27.07.2005 Bull. 21
    Invention — RU 2257610 C1

    http://www1.fips.ru/fips_servl/fips_servlet?DB=RUPAT&DocNumber=2257610&TypeFile=html

    :param int size: size of sliding windows
    :return: filter that calculates mean of polynomial approximations.
    """
    res = min_size_filter_generator(size)
    res = sum(res) / ((size - 3) / 2)
    return res


def min_size_filter_generator(size=25):
    """
    Generates the sequence of filters with different window sizes,

    Each filter compute polynomial approximations for sliding windows
    of the same sizes but starts in different points.

    This approach can be illustrated with sequences of greek letters:
        (Α)(Β, Γ)(Δ, Ε, Ζ)(Η, Θ, Ι, Κ)(Λ, Μ, Ν, Ξ)(Ο, Π …
        (Α, Β)(Γ, Δ, Ε)(Ζ, Η, Θ, Ι)(Κ, Λ, Μ, Ν)(Ξ, Ο, Π …
        (Α, Β, Γ)(Δ, Ε, Ζ, Η)(Θ, Ι, Κ, Λ)(Μ, Ν, Ξ, Ο)(Π …
        (Α, Β, Γ, Δ)(Ε, Ζ, Η, Θ, Ι)(Κ, Λ, Μ, Ν)(Ξ, Ο, Π …

    :param int size: size of sliding window and maximum delay.
    :return: sequence of filters with different minimal window sizes,
    """
    for offset in xrange(3, size, 2):
        # (3, size, 2) — is connected with a trait of
        # Savitzky-Golay algotithm to build polynomial approximation.
        # Size of window for Savitzky-Golay ought to be a odd number.
        yield polynomial_approximation(
            s=size,
            min_size=offset
        )


def simple_mole_filter(size=25):
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
    res = delay_filter_generator(size)
    res = sum(res) / size
    return res


def delay_filter_generator(size=25):
    """
    Generates the sequence of filters with different delays,

    Each filter compute polynomial approximations for sliding windows
    of the same sizes but starts in different points.

    This approach can be illustrated with sequences of greek letters:

        (Α, Β, Γ, Δ)(Ε, Ζ, Η, Θ)(Ι, Κ, Λ, Μ)(Ν, Ξ, Ο, Π)…
        ∅..(Β, Γ, Δ, Ε)(Ζ, Η, Θ, Ι)(Κ, Λ, Μ, Ν)(Ξ, Ο, Π …
        ∅.....(Γ, Δ, Ε, Ζ)(Η, Θ, Ι, Κ)(Λ, Μ, Ν, Ξ)(Ο, Π …
        ∅........(Δ, Ε, Ζ, Η)(Θ, Ι, Κ, Λ)(Μ, Ν, Ξ, Ο)(Π …

    :param int size: size of sliding window and maximum delay.
    :return: sequence of filters with different delays,
    """
    for offset in xrange(size):
        # with delay we try to reconstruct delay of sliding windows
        # to sum it window by window.
        # It is simple but not very effective.
        yield delay(offset) | same_size_polynomial_approximation(s=size)
