# -*- coding: utf8 -*-

from __future__ import absolute_import

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
        image_size, video_state = self.get_image_size(video_state, *args, **kwargs)
        vector = shrink(vector, image_size.width, image_size.height)
        return vector, video_state

    def transform_image_size(self, vector, video_state = None, *args, **kwargs):
        image_size, video_state = self.get_image_size(video_state, *args, **kwargs)
        vector = shrink(vector, image_size.width, image_size.height)
        return vector, video_state

    def frame_to_image(self, frame, video_state, *args, **kwargs):
        vector, video_state = self._frame_to_image(frame, 'rgb24', video_state, *args, **kwargs)
        return vector, video_state

    def _frame_to_image(self, frame, av_format, video_state, *args, **kwargs):
        optimized_frame, video_state = self.get_optimized_frame(
            frame,
            av_format,
            video_state,
            *args,
            **kwargs
        )
        vector = optimized_frame.to_nd_array() * 1.0
        return vector, video_state


    def get_optimized_frame(self, frame, av_format, video_state, *args, **kwargs):
        size, video_state = self.get_optimize_size(frame, video_state, *args, **kwargs)
        optimized_frame = frame.reformat(
            format  = av_format,
            width   = size.width,
            height  = size.height,
        )
        return optimized_frame, video_state


    def get_image_size(self, video_state, *args, **kwargs):
        image_size = video_state.options.get(
            'image_size',
            DEFAULT_IMAGE_SIZE
        )
        return image_size, video_state

    def get_optimize_size(self, frame, video_state, *args, **kwargs):
        '''
            Resize frame before converting to PIL.Image.
            For optimization issues width or height should be multiple by 16
        '''
        frame_size = video_state.options.get(
            'frame_size',
            DEFAULT_OPTIMIZE_FRAME_SIZE
        )
        return frame_size, video_state


    def __optimize_size(self, frame, video_state, *args, **kwargs):
        '''
            WARNING: for experiments

            Resize frame before converting to vector.
            Try to guess the best size with frame ratio.
            But it throw «libav.swscaler: Warning: data is not aligned!»
            This can lead to a speedloss.
        '''
        if not video_state.memory_cache.get('optimized_size'):
            image_size = DEFAULT_IMAGE_SIZE
            frame_dim = min(frame.width, frame.height)
            image_dim = max(image_size.width, image_size.height)
            coef = float(frame_dim) / image_dim
            ## Guess the whole coef.
            while not is_whole(coef):
                image_dim = image_dim + 1
                coef = 1.0 * frame_dim / image_dim
            coef = int(coef)
            video_state.memory_cache.optimized_size = SmartDict(
                width  = frame.width / coef,
                height = frame.height / coef
            )
        return video_state.memory_cache.optimized_size, video_state
