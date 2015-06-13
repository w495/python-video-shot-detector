# -*- coding: utf8 -*-

from __future__ import absolute_import
import scipy as sp

class Gray16ColourMixin(object):

    __COLOUR_SIZE = 1 << 16

    def frame_to_image(self, frame, video_state, *args, **kwargs):
        image, video_state = self._frame_to_image(frame, 'gray16le', video_state)
        video_state.colour_size  = self.COLOUR_SIZE
        return image, video_state

    def get_colour_size(self):
        return self.__COLOUR_SIZE

    def get_pixel_size(self):
        return self.get_colour_size()


class Gray8ColourMixin(object):

    __COLOUR_SIZE = 1 << 8

    def frame_to_image(self, frame, video_state, *args, **kwargs):
        image, video_state = self._frame_to_image(frame, 'rgb24', video_state)
        image = sp.inner(image, [299, 587, 114]) / 1000.0
        return image, video_state

    def get_colour_size(self):
        return self.__COLOUR_SIZE

    def get_pixel_size(self):
        return self.get_colour_size()


GrayColourMixin = Gray8ColourMixin
