# -*- coding: utf8 -*-

from __future__ import absolute_import

from PIL import Image

from .utils import SmartDict, is_whole, shrink


##
## Size of vector, when we deal with computing.
## For optimization issues it should be multiple by 2.
## Perhaps it is better to put in `video_state`.
##
DEFAULT_IMAGE_SIZE = SmartDict(
    width  = 4,
    height = 4,
)


##
## For optimization issues it should be multiple by 16.
## Perhaps it is better to put in `video_state`.
##
DEFAULT_OPTIMIZE_FRAME_SIZE = SmartDict(
    width  = 16,
    height = 16,
)

class BaseVectorMixin(object):

    def build_image(self, frame, video_state, *args, **kwargs):
        vector, video_state = self.frame_to_image(frame, video_state, *args, **kwargs)
        return vector, video_state

    def transform_image_size(self, vector, video_state = None, *args, **kwargs):
        #vector = shrink(vector, DEFAULT_IMAGE_SIZE.width, DEFAULT_IMAGE_SIZE.height)
        return vector, video_state

    def frame_to_image(self, frame, video_state, *args, **kwargs):
        vector, video_state = self._frame_to_image(frame, 'rgb24', video_state, *args, **kwargs)
        return vector, video_state

    def _frame_to_image(self, frame, av_format, video_state, *args, **kwargs):
        size, video_state = self.optimize_size(frame, video_state, *args, **kwargs)
        optimized_frame = frame.reformat(
            format  = av_format,
            width   = size.width,
            height  = size.height,
        )
        vector = optimized_frame.to_nd_array() * 1.0

        return vector, video_state


    def optimize_size(self, frame, video_state, *args, **kwargs):
        '''
            Resize frame before converting to PIL.Image.
            For optimization issues width or height should be multiple by 16
        '''
        return DEFAULT_OPTIMIZE_FRAME_SIZE, video_state

