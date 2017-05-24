# -*- coding: utf8 -*-
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: profile=True
# cython: nonecheck=False

"""
    ...
"""


import numpy as np

# # :formatter:on
cimport numpy as np
# # :formatter:off


ctypedef unsigned char spix_t

ctypedef spix_t[:,:,:]  simg_t

ctypedef double dpix_t

ctypedef dpix_t[:,:] dimg_t

dst_item_type = np.float64

ctypedef double coef_t

ctypedef coef_t[:] cvec_t


cdef cvec_t LUMA_COEF_VECTOR = np.array([0.299, 0.587, 0.114])


def reformat_image(simg_t src_image,
                   size_t width,
                   size_t height,
                   size_t colour_size=256,
                   cvec_t colour_coef_vector=LUMA_COEF_VECTOR,
                   size_t n_colours=0):
    """
    
    :param src_image: 
    :param width: 
    :param height: 
    :param colour_size: 
    :param colour_coef_vector: 
    :param n_colours: 
    :return: 
    """

    cdef :
        size_t fold_height, fold_width
        dimg_t dst_image
        np.ndarray[dpix_t, ndim=1] aranged_image
        np.ndarray[dpix_t, ndim=2] reshaped_image
    fold_height = src_image.shape[0] / height
    fold_width = src_image.shape[1] / width
    if n_colours == 0:
        n_colours = colour_coef_vector.shape[0]
    aranged_image = np.arange(width * height, dtype=dst_item_type)
    reshaped_image = aranged_image.reshape((width, height))
    dst_image  = fold_image(
        src_image=src_image,
        dst_image=reshaped_image,
        fold_height=fold_height,
        fold_width=fold_width,
        colour_size=colour_size,
        colour_coef_vector=colour_coef_vector,
        n_colours=n_colours
    )
    return np.asarray(dst_image)


cdef inline dimg_t fold_image(simg_t src_image,
                              dimg_t dst_image,
                              size_t fold_height,
                              size_t fold_width,
                              size_t colour_size,
                              cvec_t colour_coef_vector,
                              size_t n_colours) nogil:
    """
    
    :param src_image: 
    :param dst_image: 
    :param fold_height: 
    :param fold_width: 
    :param colour_size: 
    :param colour_coef_vector: 
    :param n_colours: 
    :return: 
    """
    cdef size_t dst_h, dst_w

    height = dst_image.shape[0]
    width = dst_image.shape[1]
    for dst_h in range(height):
        for dst_w in range(width):
            dst_image[dst_h, dst_w] = fold_pixel(
                src_image=src_image,
                dst_h=dst_h,
                dst_w=dst_w,
                fold_height=fold_height,
                fold_width=fold_width,
                colour_size=colour_size,
                colour_coef_vector=colour_coef_vector,
                n_colours=n_colours,
            )
    return dst_image




cdef inline dpix_t fold_pixel(simg_t src_image,
                              size_t dst_h,
                              size_t dst_w,
                              size_t fold_height,
                              size_t fold_width,
                              size_t colour_size,
                              cvec_t colour_coef_vector,
                              size_t n_colours) nogil:
    """
    
    :param src_image: 
    :param dst_h: 
    :param dst_w: 
    :param fold_height: 
    :param fold_width: 
    :param colour_size: 
    :param colour_coef_vector: 
    :param n_colours: 
    :return: 
    """


    cdef :
        size_t h, w, colour
        size_t height_offset, width_offset
        spix_t src_item
        dpix_t dst_item, luma_item
        dpix_t shrunk_item

    height_offset = dst_h * fold_height
    width_offset = dst_w * fold_width

    shrunk_item = 0.0
    for h in range(height_offset, height_offset + fold_height):
        for w in range(width_offset, width_offset + fold_width):
            for colour in range(n_colours):
                src_item = src_image[h, w, colour]
                luma_item = colour_coef_vector[colour]
                dst_item = src_item * luma_item
                shrunk_item += dst_item
    shrunk_item = shrunk_item / (fold_height * fold_width)
    shrunk_item = shrunk_item / colour_size
    return shrunk_item
