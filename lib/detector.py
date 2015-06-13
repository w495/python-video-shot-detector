# -*- coding: utf8 -*-

from __future__ import absolute_import

from .base_detector import BaseDetector, BaseShotState

DEFAULT_IMAGE_SIZE = (5, 5)

class ImageState(object):
    size = DEFAULT_IMAGE_SIZE

class ShotState(BaseShotState):
    image_state = ImageState()

class Detector(BaseDetector):

    def build_shot_state(self):
        return BaseImageShotState()

    def build_image(self, frame, shot_state):
        return frame.to_image(), shot_state

    def transform_image_size(self, image, shot_state = None):
        image_size = shot_state.image_state.size
        return image.resize(image_size,), shot_state
