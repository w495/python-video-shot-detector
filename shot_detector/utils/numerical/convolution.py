# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from .gaussian_kernel import gaussian_kernel_1d


def gaussian_1d_convolve(vector, size=None, sigma=None, offset=None):
    """

    :param vector: 
    :param size: 
    :param sigma: 
    :param offset: 
    :return: 
    """
    if size is None:
        size = len(vector)
    kernel = gaussian_kernel_1d(size, sigma, offset)
    # convolution = np.convolve(vector, kernel, 'valid')
    convolution = convolve_1d_vector(vector, kernel)
    return convolution


def convolve_1d_vector(vector, kernel):
    """
    Do the same that `np.convolve(vector, kernel, 'valid')`
    but works with nested vectors

    :param vector: array or list of arrays
    :param kernel: array or list of arrays
    :return: convolution
    """
    vector_size = len(vector)
    kernel_size = len(kernel)
    convolution = []
    for item in vector:
        for kernel_item in kernel:
            convolution += [item * kernel_item]
    out_size = max(vector_size, kernel_size) - min(vector_size,
                                                   kernel_size) + 1
    blind_area = (vector_size * kernel_size - out_size) // 2
    if blind_area:
        convolution = convolution[blind_area:-blind_area]
    return convolution
