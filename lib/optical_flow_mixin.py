# -*- coding: utf8 -*-

from __future__ import absolute_import

import math

import numpy as np
from scipy.signal import convolve, convolve2d

class OpticalFlowMixin(object):

    def build_features(self, image, video_state = None, *args, **kwargs):
        ## TODO
        return None, video_state

def gauss_kern():
    h1 = 15
    h2 = 15
    x, y = np.mgrid[0:h2, 0:h1]
    x = x - h2/2
    y = y - h1/2
    sigma = 1.5
    g = np.exp( -( x**2 + y**2 ) / (2*sigma**2) );
    return g / g.sum()

def deriv(im1, im2):
    g = gauss_kern()
    Img_smooth = convolve(im1,g,mode='same')
    fx, fy = np.gradient(Img_smooth)
    ft = convolve2d(im1, 0.25 * np.ones((2,2))) + \
         convolve2d(im2, -0.25 * np.ones((2,2)))
    fx = fx[0: fx.shape[0] - 1, 0: fx.shape[1] - 1]
    fy = fy[0: fy.shape[0] - 1, 0: fy.shape[1] - 1];
    ft = ft[0: ft.shape[0] - 1, 0: ft.shape[1] - 1];
    return fx, fy, ft

def lucas_kanade(im1, im2, i, j, window_size) :
   fx, fy, ft = deriv(im1, im2)
   half_win = np.floor(window_size/2)
   cur_fx = fx[i - half_win - 1: i + half_win, j - half_win-1: j + half_win]
   cur_fy = fy[i - half_win - 1: i + half_win, j - half_win-1: j + half_win]
   cur_ft = ft[i - half_win - 1: i + half_win, j - half_win-1: j + half_win]
   cur_fx = cur_fx.T
   cur_fy = cur_fy.T
   cur_ft = cur_ft.T

   cur_fx = cur_fx.flatten(order='F')
   cur_fy = cur_fy.flatten(order='F')
   cur_ft = -cur_ft.flatten(order='F')

   A = np.vstack((cur_fx, cur_fy)).T
   U = np.dot(np.dot(np.linalg.pinv(np.dot(A.T,A)),A.T),cur_ft)
   return U[0], U[1]
