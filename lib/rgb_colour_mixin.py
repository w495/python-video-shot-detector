# -*- coding: utf8 -*-

from __future__ import absolute_import


class RgbColourMixin(object):

    __COLOUR_SIZE = 1 << 8

    def frame_to_image(self, frame, video_state):
        image, video_state = self._frame_to_image(frame, 'rgb24', video_state)
        return image, video_state

    def get_colour_size(self):
        return self.__COLOUR_SIZE

    def get_pixel_size(self):
        return self.get_colour_size() * 3
