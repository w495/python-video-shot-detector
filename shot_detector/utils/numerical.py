# -*- coding: utf8 -*-


from __future__ import absolute_import, division, print_function

import numpy as np
import skimage.filters


def histogram(*args, **kwargs):
    return np.histogram(*args, **kwargs)


def threshold_otsu(image):
    threshold_global_otsu = skimage.filters.threshold_otsu(image)
    otsu_vector = image >= threshold_global_otsu
    return otsu_vector


def shrink(data, cols, rows):
    row_sp = data.shape[0] // rows
    col_sp = data.shape[1] // cols
    if 1 == row_sp == col_sp:
        return data
    shrunk = np.zeros((rows, cols))
    for i in xrange(0, rows):
        for j in xrange(0, cols):
            zz = data[i * row_sp: i * row_sp + row_sp, j * col_sp: j * col_sp + col_sp]
            shrunk[i, j] = np.sum(zz) / (zz.shape[0] * zz.shape[1])
    return shrunk


def shrink__(data, rows, cols):
    row_sp = data.shape[0] // rows
    col_sp = data.shape[1] // cols
    reshaped = data.reshape(rows, row_sp, cols, col_sp)

    return reshaped.sum(axis=1).sum(axis=2)


def shrink__2(data, cols, rows):
    width = data.shape[0]
    height = data.shape[1]
    row_sp = width // rows
    col_sp = height // cols
    print(row_sp, col_sp)

    for i in xrange(row_sp):
        Z = data[i::row_sp]
        print(i, row_sp + i * width, width, Z.shape)

    if 1 == row_sp == col_sp:
        return data
    tmp = np.sum(1.0 * data[i::row_sp] // row_sp for i in xrange(row_sp))
    return np.sum(1.0 * tmp[:, i::col_sp] // col_sp for i in xrange(col_sp))


def histogram_intersect(h1, h2):
    res = []
    for i, j in zip(h1, h2):
        q = min(i, j)
        res += [q]
    return res


def gaussian_1d_convolve(vector, size=None, sigma=None, offset=None, mode='valid'):
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
    out_size = max(vector_size, kernel_size) - min(vector_size, kernel_size) + 1
    blind_area = (vector_size * kernel_size - out_size) // 2
    if blind_area:
        convolution = convolution[blind_area:-blind_area]
    return convolution

def gaussian_kernel_1d(size=5, sigma=None, offset = None):
    """
    Returns a normalized 1D gauss kernel array for convolutions.
    """
    size = int(size)
    if offset is None:
        offset = size // 2
    x = np.mgrid[0:size]
    x += -offset
    divisor = float(size)
    if sigma:
        divisor = 2 * (sigma ** 2)
    g = np.exp(-((x ** 2) / divisor))
    return list(g / g.sum())


def gaussian_kernel_2d(size=5, size_y=None, sigma=None, sigma_y=None):
    """
    Returns a normalized 2D gauss kernel array for convolutions
    From http://www.scipy.org/Cookbook/SignalSmooth
    """
    size = int(size)
    if not size_y:
        size_y = size
    else:
        size_y = int(size_y)
    x, y = np.mgrid[0:size, 0:size_y]
    x -= size // 2
    y -= size_y // 2
    divisor_x = float(size)
    divisor_y = float(size_y)
    if (sigma):
        if not sigma_y:
            sigma_y = sigma
        else:
            sigma_y = int(sigma_y)
        divisor_x = 2 * (sigma ** 2)
        divisor_y = 2 * (sigma_y ** 2)
    g = np.exp(-((x ** 2) / divisor_x + (y ** 2) / divisor_y))
    return g / g.sum()


def deriv(im1, im2):
    g = gaussian_kernel_2d(size=15, sigma=1.5)
    img_smooth = np.convolve(im1, g, mode='same')
    fx, fy = np.gradient(img_smooth)
    ft = np.convolve2d(im1, 0.25 * np.ones((2, 2))) + \
         np.convolve2d(im2, -0.25 * np.ones((2, 2)))
    fx = fx[0: fx.shape[0] - 1, 0: fx.shape[1] - 1]
    fy = fy[0: fy.shape[0] - 1, 0: fy.shape[1] - 1];
    ft = ft[0: ft.shape[0] - 1, 0: ft.shape[1] - 1];
    return fx, fy, ft


def lucas_kanade_point(im1, im2, i=2, j=2, window_size=3.0):
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
    cur_fx = fx[i - half_win - 1: i + half_win, j - half_win - 1: j + half_win]
    cur_fy = fy[i - half_win - 1: i + half_win, j - half_win - 1: j + half_win]
    cur_ft = ft[i - half_win - 1: i + half_win, j - half_win - 1: j + half_win]
    cur_fx = cur_fx.T
    cur_fy = cur_fy.T
    cur_ft = cur_ft.T
    cur_fx = cur_fx.flatten(order='F')
    cur_fy = cur_fy.flatten(order='F')
    cur_ft = -cur_ft.flatten(order='F')
    A = np.vstack((cur_fx, cur_fy)).T
    dot1 = np.dot(A.T, A)
    pinv = np.linalg.pinv(dot1)
    dot2 = np.dot(pinv, A.T)
    U = np.dot(dot2, cur_ft)
    return U[0], U[1]


def lucas_kanade(im1, im2, win=1):
    assert im1.shape == im2.shape
    I_x = np.zeros(im1.shape)
    I_y = np.zeros(im1.shape)
    I_t = np.zeros(im1.shape)
    I_x[1:-1, 1:-1] = (im1[1:-1, 2:] - im1[1:-1, :-2]) / 2
    I_y[1:-1, 1:-1] = (im1[2:, 1:-1] - im1[:-2, 1:-1]) / 2
    I_t[1:-1, 1:-1] = im1[1:-1, 1:-1] - im2[1:-1, 1:-1]
    params = np.zeros(im1.shape + (5,))  # Ix2, Iy2, Ixy, Ixt, Iyt
    params[..., 0] = I_x * I_x  # I_x2
    params[..., 1] = I_y * I_y  # I_y2
    params[..., 2] = I_x * I_y  # I_xy
    params[..., 3] = I_x * I_t  # I_xt
    params[..., 4] = I_y * I_t  # I_yt
    del I_x, I_y, I_t
    cum_params = np.cumsum(np.cumsum(params, axis=0), axis=1)
    del params
    win_params = (cum_params[2 * win + 1:, 2 * win + 1:] -
                  cum_params[2 * win + 1:, :-1 - 2 * win] -
                  cum_params[:-1 - 2 * win, 2 * win + 1:] +
                  cum_params[:-1 - 2 * win, :-1 - 2 * win])
    del cum_params
    op_flow = np.zeros(im1.shape + (2,))
    det = win_params[..., 0] * win_params[..., 1] - win_params[..., 2] ** 2
    op_flow_x = np.where(det != 0,
                         (win_params[..., 1] * win_params[..., 3] -
                          win_params[..., 2] * win_params[..., 4]) / det,
                         0)
    op_flow_y = np.where(det != 0,
                         (win_params[..., 0] * win_params[..., 4] -
                          win_params[..., 2] * win_params[..., 3]) / det,
                         0)
    op_flow[win + 1:-1 - win, win + 1:-1 - win, 0] = op_flow_x[:-1, :-1]
    op_flow[win + 1:-1 - win, win + 1:-1 - win, 1] = op_flow_y[:-1, :-1]
    return op_flow


if (__name__ == '__main__'):

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
            print(arr_x[0], )
        print()

    print()
    for arr_y in lk:
        for arr_x in arr_y:
            # for arr_z in arr_x:
            print(arr_x[1], )
        print()
