# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import numpy as np


def deriv(im1, im2):
    """

    :param im1:
    :param im2:
    :return:
    """
    g = gaussian_kernel_2d(size=15, sigma=1.5)
    img_smooth = np.convolve(im1, g, mode='same')
    fx, fy = np.gradient(img_smooth)

    ft1 = np.convolve(im1, 0.25 * np.ones((2, 2)))
    ft2 = np.convolve(im2, -0.25 * np.ones((2, 2)))
    ft = ft1 + ft2

    fx = fx[0: fx.shape[0] - 1, 0: fx.shape[1] - 1]
    fy = fy[0: fy.shape[0] - 1, 0: fy.shape[1] - 1]
    ft = ft[0: ft.shape[0] - 1, 0: ft.shape[1] - 1]
    return fx, fy, ft


def lucas_kanade_point(im1, im2, i=2, j=2, window_size=3.0):
    """

    :param im1:
    :param im2:
    :param i:
    :param j:
    :param window_size:
    :return:
    """
    assert im1.shape == im2.shape
    fx, fy, ft = deriv(im1, im2)
    half_win = np.floor(window_size / 2)
    if i <= half_win:
        i += half_win - i
    if j <= half_win:
        j += half_win - j
    if i >= (im1.shape[0] - half_win):
        i -= half_win
    if j >= (im1.shape[1] - half_win):
        j -= half_win
    # noinspection PyPep8
    cur_fx = fx[i - half_win - 1: i + half_win,
             j - half_win - 1: j + half_win]
    # noinspection PyPep8
    cur_fy = fy[i - half_win - 1: i + half_win,
             j - half_win - 1: j + half_win]
    # noinspection PyPep8
    cur_ft = ft[i - half_win - 1: i + half_win,
             j - half_win - 1: j + half_win]
    cur_fx = cur_fx.T
    cur_fy = cur_fy.T
    cur_ft = cur_ft.T
    cur_fx = cur_fx.flatten(order='F')
    cur_fy = cur_fy.flatten(order='F')
    cur_ft = -cur_ft.flatten(order='F')
    a_ = np.vstack((cur_fx, cur_fy)).T
    dot1 = np.dot(a_.T, a_)
    pinv = np.linalg.pinv(dot1)
    dot2 = np.dot(pinv, a_.T)
    u_ = np.dot(dot2, cur_ft)
    return u_[0], u_[1]


# noinspection PyTypeChecker
def lucas_kanade(im1, im2, win=1):
    """

    :param im1:
    :param im2:
    :param win:
    :return:
    """
    assert im1.shape == im2.shape
    i_x = np.zeros(im1.shape)
    i_y = np.zeros(im1.shape)
    i_t = np.zeros(im1.shape)
    i_x[1:-1, 1:-1] = (im1[1:-1, 2:] - im1[1:-1, :-2]) / 2
    i_y[1:-1, 1:-1] = (im1[2:, 1:-1] - im1[:-2, 1:-1]) / 2
    i_t[1:-1, 1:-1] = im1[1:-1, 1:-1] - im2[1:-1, 1:-1]
    params = np.zeros(im1.shape + (5,))  # Ix2, Iy2, Ixy, Ixt, Iyt
    params[..., 0] = i_x * i_x  # I_x2
    params[..., 1] = i_y * i_y  # I_y2
    params[..., 2] = i_x * i_y  # I_xy
    params[..., 3] = i_x * i_t  # I_xt
    params[..., 4] = i_y * i_t  # I_yt
    del i_x, i_y, i_t
    cum_params = np.cumsum(np.cumsum(params, axis=0), axis=1)
    del params
    win_params = (cum_params[2 * win + 1:, 2 * win + 1:] -
                  cum_params[2 * win + 1:, :-1 - 2 * win] -
                  cum_params[:-1 - 2 * win, 2 * win + 1:] +
                  cum_params[:-1 - 2 * win, :-1 - 2 * win])
    del cum_params
    op_flow = np.zeros(im1.shape + (2,))
    det = win_params[..., 0] * win_params[..., 1] - win_params[
                                                        ..., 2] ** 2
    op_flow_x = np.where(det != 0,
                         (win_params[..., 1] * win_params[..., 3] -
                          win_params[..., 2] * win_params[
                              ..., 4]) / det)
    op_flow_y = np.where(det != 0,
                         (win_params[..., 0] * win_params[..., 4] -
                          win_params[..., 2] * win_params[
                              ..., 3]) / det)
    op_flow[win + 1:-1 - win, win + 1:-1 - win, 0] = op_flow_x[:-1, :-1]
    op_flow[win + 1:-1 - win, win + 1:-1 - win, 1] = op_flow_y[:-1, :-1]
    return op_flow


if __name__ == '__main__':

    x = 1.0 * np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    y = 1.0 * np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    lk = lucas_kanade(x, y)

    for arr_y in lk:
        for arr_x in arr_y:
            # for arr_z in arr_x:
            pass

    for arr_y in lk:
        for arr_x in arr_y:
            # for arr_z in arr_x:
            pass
