# -*- coding: utf8 -*-

from __future__ import absolute_import

from PIL import Image

from .utils import SmartDict, is_whole

##
## Size of image, when we deal with computing.
## Perhaps it is better to put in `shot_state`.
##
DEFAULT_IMAGE_SIZE = SmartDict(
    width  = 5,
    height = 5,
)

##
## For optimization issues it should be multiple by 16.
## Perhaps it is better to put in `shot_state`.
##
DEFAULT_OPTIMIZE_FRAME_SIZE = SmartDict(
    width  = 16,
    height = 16,
)

AV2PIL_FORMAT_DICT = {
    'gray'   : 'L',
    'gray16le' : 'L',
    'rgb24' : 'RGB',
}

class BaseImageMixin(object):

    def build_image(self, frame, shot_state, *args, **kwargs):
        image, shot_state = self.frame_to_image(frame, shot_state, *args, **kwargs)
        return image, shot_state

    def transform_image_size(self, image, shot_state = None, *args, **kwargs):
        '''
            Resize frame after converting to PIL.Image.
            Should be used with optimized size before.
        '''
        image_size = DEFAULT_IMAGE_SIZE
        image = image.resize((image_size.width, image_size.height),)
        return image, shot_state

    def frame_to_image(self, frame, shot_state, *args, **kwargs):
        image, shot_state = self._frame_to_image(frame, 'rgb24', shot_state, *args, **kwargs)
        return image, shot_state

    def _frame_to_image(self, frame, av_format, shot_state, *args, **kwargs):
        pil_format = AV2PIL_FORMAT_DICT.get(av_format, 'RGB')
        size, shot_state = self.optimize_size(frame, shot_state, *args, **kwargs)
        plane = frame.reformat(
            format  = av_format,
            width   = size.width,
            height  = size.height,
        ).planes[0]
        image = Image.frombuffer(
            pil_format,
            (size.width, size.height),
            plane,
            "raw",
            pil_format,
            0,
            1
        )
        return image, shot_state


    def optimize_size(self, frame, shot_state, *args, **kwargs):
        '''
            Resize frame before converting to PIL.Image.
            For optimization issues width or height should be multiple by 16
        '''
        return DEFAULT_OPTIMIZE_FRAME_SIZE, shot_state


    def __optimize_size(self, frame, shot_state, *args, **kwargs):
        '''
            Resize frame before converting to PIL.Image.
            Try to guess the best size with frame ratio.
            But it throw «libav.swscaler: Warning: data is not aligned!»
            This can lead to a speedloss.
        '''
        if not shot_state.memory_cache.get('optimized_size'):
            image_size = DEFAULT_IMAGE_SIZE
            frame_dim = min(frame.width, frame.height)
            image_dim = max(image_size.width, image_size.height)
            coef = float(frame_dim) / image_dim
            ## Guess the whole coef.
            while not is_whole(coef):
                image_dim = image_dim + 1
                coef = 1.0 * frame_dim / image_dim
            coef = int(coef)
            shot_state.memory_cache.optimized_size = SmartDict(
                width  = frame.width / coef,
                height = frame.height / coef
            )
        return shot_state.memory_cache.optimized_size, shot_state

