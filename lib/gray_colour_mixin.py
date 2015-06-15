# -*- coding: utf8 -*-

from __future__ import absolute_import
import scipy as sp

from .base_vector_mixin import BaseVectorMixin
from .base_image_mixin  import BaseImageMixin



class Gray16ColourMixin(object):

    def build_image(self, frame, video_state, *args, **kwargs):
        image, video_state = self.frame_to_image(frame, 'gray16le', video_state)
        return image, video_state

class Gray8ColourMixin(BaseVectorMixin):

    def build_image(self, frame, video_state, *args, **kwargs):
        image, video_state = self.frame_to_image(frame, 'rgb24', video_state)
        image, video_state = self.convert_to_luminosity(image, video_state, *args, **kwargs)
        return image, video_state


GrayColourMixin = Gray8ColourMixin
