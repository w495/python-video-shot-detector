# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.handlers import BaseVideoHandler, BaseEventHandler


class BaseShotDetector(BaseVideoHandler, BaseEventHandler):

    __logger = logging.getLogger(__name__)


    def detect(self, input_uri='', format_name=None, **kwargs):
        """
        :param str input_uri:
            file name of input video or path to resource
            for example `http://localhost:8090/live.flv`
            You can use any string, that can be accepted
            by input ffmpeg-parameter. For example:
                'http://localhost:8090/live.flv',
        :param str format_name:
            name of video format. Use it for haerdware devices
        :param dict kwargs: any options for consecutive methods,
            ignores it and pass it through
        :return:
        """
        video_state = self.handle_video(
            input_uri=input_uri,
            format_name=format_name,
            **kwargs
        )
        return video_state
