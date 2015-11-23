# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import numpy as np

from shot_detector.utils.collections import SmartDict

from shot_detector.utils.common import is_whole
from shot_detector.utils.numerical import shrink

from shot_detector.utils.iter import handle_content


from .base_extractor import BaseExtractor


# #
# # Size of vector, when we deal with computing.
# # For optimization issues it should be multiple by 2.
# # Perhaps it is better to put in `video_state`.
# #
DEFAULT_IMAGE_SIZE = SmartDict(
    width=16,
    height=16,
)

# #
# # For optimization issues it should be multiple by 8.
# # Perhaps it is better to put in `video_state`.
# #
DEFAULT_OPTIMIZE_FRAME_SIZE = SmartDict(
    width=16,
    height=16,
)

AV_FORMAT_COLOUR_SIZE = SmartDict(
    rgb24=(1 << 8),
    gray16le=(1 << 16),
)


class VectorBased(BaseExtractor):


    def __frame_features(self, frame_iterable, **kwargs):
        frame_repr_iterable = (frame.source for frame in frame_iterable)


    def feature_sources(self, frame_iterable, **kwargs):
        return self.av_frames(frame_iterable, **kwargs)


    @staticmethod
    def av_frames(frame_iterable, **kwargs):
        for frame in frame_iterable:
            yield frame.source

    def optimize_frames(self, av_frame_iterable, av_format='rgb24', **kwargs):
        frame_size = self.frame_size(**kwargs)
        for av_frame in av_frame_iterable:
            yield av_frame.reformat(
                format=av_format,
                width=frame_size.width,
                height=frame_size.height,
            )

    def raw_image(self, av_frame_iterable, **kwargs):
        for av_frame in av_frame_iterable:
            image = av_frame.to_nd_array() * 1.0
            yield image

    def normalize_images(self, image_iterable, **kwargs):
        colour_size = self.colour_size(**kwargs)
        for image in image_iterable:
            image = image / colour_size
            yield image

    def shrink_images(self, image_iterable, **kwargs):
        image_size = self.image_size(**kwargs)
        for image in image_iterable:
            image = shrink(image, image_size)
            yield image

    @staticmethod
    def colour_size(colour_size=None, av_format='rgb24', **kwargs):
        if colour_size is None:
            colour_size = AV_FORMAT_COLOUR_SIZE.get(av_format, 256)
        return colour_size

    @staticmethod
    def frame_size(frame_size=None, av_format='rgb24'):
        if frame_size is None:
            frame_size = DEFAULT_OPTIMIZE_FRAME_SIZE
        return frame_size

    @staticmethod
    def image_size(image_size=None, av_format='rgb24'):
        if image_size is None:
            image_size = DEFAULT_IMAGE_SIZE
        return image_size


    def extract_frame_features(self, frame, video_state, *args, **kwargs):

        #print ('extract_frame_features frame = ', frame)

        image, video_state = self.build_image(frame, video_state)
        features, video_state = self.handle_image(image, video_state, *args, **kwargs)
        return features, video_state

    def handle_image(self, image, video_state, *args, **kwargs):
        image, video_state = self.transform_image(image, video_state)
        features, video_state = self.handle_transformed_image(image, video_state)
        video_state = self.store_sizes(image, video_state, *args, **kwargs)
        return features, video_state

    def handle_transformed_image(self, image, video_state, *args, **kwargs):
        features, video_state = self.build_features(image, video_state)
        features, video_state = self.handle_features(features, video_state)
        return features, video_state

    def handle_features(self, features, video_state, *args, **kwargs):
        features, video_state = self.transform_features(features, video_state)
        return features, video_state


    def build_image(self, frame, video_state, *args, **kwargs):
        vector, video_state = self.frame_to_image(frame, 'rgb24', video_state, *args, **kwargs)
        return vector, video_state

    def transform_image_size(self, vector, video_state, *args, **kwargs):
        image_size, video_state = self.get_image_size(video_state, *args, **kwargs)
        vector = shrink(vector, image_size.width, image_size.height)
        return vector, video_state

    def frame_to_image(self, frame, av_format, video_state, *args, **kwargs):
        #print ('vector = ', frame, av_format, args, kwargs)

        optimized_frame, video_state = self.get_optimized_frame(
            frame,
            av_format,
            video_state,
            *args,
            **kwargs
        )
        raw_vector = optimized_frame.to_nd_array() * 1.0
        #print ('raw_vector = ', raw_vector)

        vector, video_state = self.normalize_colour(raw_vector, video_state)
        return vector, video_state

    def normalize_colour(self, raw_vector, video_state, *args, **kwargs):
        colour_size, video_state = self.get_colour_size(raw_vector, video_state)
        #print ('colour_size = ', colour_size)

        vector = raw_vector / colour_size
        return vector, video_state

    def get_optimized_frame(self, frame, av_format, video_state, *args, **kwargs):
        size, video_state = self.get_optimize_size(frame, video_state, *args, **kwargs)
        optimized_frame = frame.reformat(
            format=av_format,
            width=size.width,
            height=size.height,
        )
        #print ('optimized_frame  =', optimized_frame, av_format, size)
        video_state.av_format = av_format
        return optimized_frame, video_state

    def get_image_size(self, video_state, *args, **kwargs):
        image_size = video_state.options.get(
            'image_size',
            DEFAULT_IMAGE_SIZE
        )
        video_state.options.image_size = image_size
        return image_size, video_state

    def get_optimize_size(self, frame, video_state, *args, **kwargs):
        """
            Resize frame before converting to PIL.Image.
            For optimization issues width or height should be multiple by 16
        """
        frame_size = video_state.options.get(
            'frame_size',
            DEFAULT_OPTIMIZE_FRAME_SIZE
        )
        video_state.options.frame_size = frame_size
        return frame_size, video_state

    def colour_histogram(self, image, video_state, histogram_kwargs={}, *args, **kwargs):
        pixel_size, video_state = self.get_raw_pixel_size(image, video_state, *args, **kwargs)
        bins = xrange(pixel_size + 1)
        histogram_vector, bin_edges = np.histogram(
            image,
            #bins=histogram_kwargs.get('bins', bins),
            **histogram_kwargs
        )
        return histogram_vector, video_state

    def convert_to_luminosity(self, image, video_state, *args, **kwargs):
        image = np.inner(image, [299, 587, 114]) / 1000.0
        return image, video_state

    def get_colour_size(self, image, video_state, *args, **kwargs):
        colour_size, video_state = self.get_raw_colour_size(image, video_state, *args, **kwargs)
        return colour_size, video_state

    def get_raw_colour_size(self, image, video_state, *args, **kwargs):
        colour_size = AV_FORMAT_COLOUR_SIZE.get(video_state.av_format, 256)
        return colour_size, video_state

    def get_raw_pixel_size(self, image, video_state, *args, **kwargs):
        pixel_size, video_state = self.get_raw_colour_size(image, video_state, *args, **kwargs)
        psize = image.shape[2:]
        if (psize):
            pixel_size = pixel_size * psize[0]
        return pixel_size, video_state

    def normalize_vector_size(self, vector):
        rng = vector.max() - vector.min()
        amin = vector.min()
        return (vector - amin)  / rng

    def __optimize_size(self, frame, video_state, *args, **kwargs):
        """
            WARNING: for experiments

            Resize frame before converting to vector.
            Try to guess the best size with frame ratio.
            But it throw «libav.swscaler: Warning: data is not aligned!»
            This can lead to a speedloss.
        """
        if not video_state.memory_cache.get('optimized_size'):
            image_size = DEFAULT_IMAGE_SIZE
            frame_dim = min(frame.width, frame.height)
            image_dim = max(image_size.width, image_size.height)
            coef = float(frame_dim) / image_dim
            # # Guess the whole coef.
            while not is_whole(coef):
                image_dim = image_dim + 1
                coef = 1.0 * frame_dim / image_dim
            coef = int(coef)
            video_state.memory_cache.optimized_size = SmartDict(
                width=frame.width / coef,
                height=frame.height / coef
            )
        return video_state.memory_cache.optimized_size, video_state
