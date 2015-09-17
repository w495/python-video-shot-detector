# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from PIL import Image

from .vector_based import VectorBased

AV2PIL_FORMAT_DICT = {
    'gray'      : 'L',
    'gray16le'  : 'L',
    'rgb24'     : 'RGB',
}

class ImageBased(VectorBased):

    def transform_image_size(self, image, video_state = None, *args, **kwargs):
        """
            Resize frame after converting to PIL.Image.
            Should be used with optimized size before.
        """
        image_size, video_state = self.get_image_size(video_state, *args, **kwargs)
        image = image.resize((image_size.width, image_size.height),)
        return image, video_state

    def frame_to_image(self, frame, av_format, video_state, *args, **kwargs):
        pil_format = AV2PIL_FORMAT_DICT.get(av_format, 'RGB')
        optimized_frame, video_state = self.get_optimized_frame(
            frame,
            av_format,
            video_state,
            *args,
            **kwargs
        )
        plane = optimized_frame.planes[0]
        image = Image.frombuffer(
            pil_format,
            (optimized_frame.width, optimized_frame.height),
            plane,
            "raw",
            pil_format,
            0,
            1
        )
        return image, video_state

    def colour_histogram(self, image, video_state = None, histogram_kwargs={}, *args, **kwargs):
        histogram_vector = image.histogram()
        return histogram_vector, video_state

    def convert_to_luminosity(self, image, video_state, *args, **kwargs):
        image = image.convert('L')
        return image, video_state

    def get_raw_pixel_size(self, image, video_state, *args, **kwargs):
        colour_size = self.get_raw_colour_size(*args, **kwargs)
        pixel_size = colour_size * len(im.getbands())
        return pixel_size, video_state

