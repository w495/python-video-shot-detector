# -*- coding: utf8 -*-

from __future__ import absolute_import

from PIL import Image

from .utils import SmartDict, is_whole

from .base_vector_mixin import BaseVectorMixin


AV2PIL_FORMAT_DICT = {
    'gray'   : 'L',
    'gray16le' : 'L',
    'rgb24' : 'RGB',
}

class BaseImageMixin(BaseVectorMixin):

    def transform_image_size(self, vector, video_state = None, *args, **kwargs):
        '''
            Resize frame after converting to PIL.Image.
            Should be used with optimized size before.
        '''
        image_size, video_state = self.get_image_size(video_state, *args, **kwargs)
        image = image.resize((image_size.width, image_size.height),)
        return vector, video_state

    def _frame_to_image(self, frame, av_format, video_state, *args, **kwargs):
        pil_format = AV2PIL_FORMAT_DICT.get(av_format, 'RGB')
        optimized_frame = self.get_optimized_frame(
            frame,
            av_format,
            video_state,
            *args,
            **kwargs
        )
        plane = optimized_frame.planes[0]
        image = Image.frombuffer(
            pil_format,
            (size.width, size.height),
            plane,
            "raw",
            pil_format,
            0,
            1
        )
        return image, video_state




