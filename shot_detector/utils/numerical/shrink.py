# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from builtins import range

import numpy as np


def naive_shrink(data, cols, rows):
    """

    Basic variant from: https://stackoverflow.com/q/10685654
    
    
    :param np.ndarray data: 
    :param int cols: 
    :param int rows: 
    :rtype: np.ndarray
    :return: 
    """

    row_sp = data.shape[0] // rows
    col_sp = data.shape[1] // cols
    other_sp = data.shape[2:]
    if 1 == row_sp == col_sp:
        return data
    shrunk = np.zeros((rows, cols) + other_sp)
    for i in range(0, rows):
        row_offset = i * row_sp
        for j in range(0, cols):
            col_offset = i * row_sp
            zz = data[
                 row_offset: row_offset + row_sp,
                 col_offset: col_offset + col_sp
                 ]
            zz_sum = np.sum(zz, axis=(0, 1))
            shrunk[i, j] = zz_sum / (row_sp * col_sp)
    return shrunk


def slice_shrink(data, cols, rows):
    """

    Variant from: https://stackoverflow.com/a/10685785
    It slower then `naive_shrink`.

    :param np.ndarray data: 
    :param int cols: 
    :param int rows: 
    :rtype: np.ndarray
    :return: 
    """

    row_sp = data.shape[0] // rows
    col_sp = data.shape[1] // cols

    if 1 == row_sp == col_sp:
        return data
    row_res = np.sum(
        data[i::row_sp] / row_sp for i in range(row_sp)
    )
    col_res = np.sum(
        row_res[:, i::col_sp] / col_sp for i in range(col_sp)
    )
    return col_res


def reshape_shrink(data, rows, cols):
    """

    Variant from: https://stackoverflow.com/a/10685869
    It faster then `naive_shrink`.
        
    :param np.ndarray data: 
    :param int cols: 
    :param int rows: 
    :rtype: np.ndarray
    :return: 
    """

    row_sp = data.shape[0] // rows
    col_sp = data.shape[1] // cols
    other_sp = data.shape[2:]
    new_shape = (rows, row_sp, cols, col_sp)
    reshaped = np.reshape(data, new_shape + other_sp)
    summed = reshaped.sum(axis=1).sum(axis=2)
    result = summed / float(row_sp * col_sp)
    return result


def shrink(data, cols, rows):
    """
    
    :param np.ndarray data: 
    :param int cols: 
    :param int rows: 
    :rtype: np.ndarray
    :return: 
    """
    result = reshape_shrink(data, cols, rows)
    return result
