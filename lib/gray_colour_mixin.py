# -*- coding: utf8 -*-

from __future__ import absolute_import
import scipy as sp

class Gray16ColourMixin(object):

    __COLOUR_SIZE = 1 << 16

    def frame_to_image(self, frame, shot_state, *args, **kwargs):
        image, shot_state = self._frame_to_image(frame, 'gray16le', shot_state)
        shot_state.colour_size  = self.COLOUR_SIZE
        return image, shot_state

    def get_colour_size(self):
        return self.__COLOUR_SIZE

    def get_pixel_size(self):
        return self.get_colour_size()


class Gray8ColourMixin(object):

    __COLOUR_SIZE = 1 << 8

    def frame_to_image(self, frame, shot_state, *args, **kwargs):
        image, shot_state = self._frame_to_image(frame, 'rgb24', shot_state)
        image = sp.inner(image, [299, 587, 114]) / 1000.0
        return image, shot_state

    def get_colour_size(self):
        return self.__COLOUR_SIZE

    def get_pixel_size(self):
        return self.get_colour_size()


GrayColourMixin = Gray8ColourMixin
