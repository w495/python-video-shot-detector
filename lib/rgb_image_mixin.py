# -*- coding: utf8 -*-

from __future__ import absolute_import

from .base_image_mixin import BaseImageMixin


class RgbImageMixin(BaseImageMixin):

    def frame_to_image(self, frame, shot_state):
        image, shot_state = self._frame_to_image(frame, 'RGB', shot_state)
        return image, shot_state
