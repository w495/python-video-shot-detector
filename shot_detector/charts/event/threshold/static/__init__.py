# -*- coding: utf8 -*-

"""
    Filters with Static Threshold

    **Ideas:**
        1. The difference between neighboring values (at some rate);
        2. Preset a threshold;
        3. Exceeding the threshold is an «anomaly».
        
    **Pros:**
        1. Easy to implement;
        2. Not demanding of resources.
        
    **Cons:**
        1. It is required to know the threshold in advance;
        2. Not applicable for different video types;
        3. Sensitive to random bursts;
        4. Catch only short-term events.
        
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from .chi_event_chart import ChiRescalingEventChart
from .ffmpeg_like_event_chart import FfmpegLikeEventChart
from .rescaling_event_chart import RescalingEventChart
from .rescaling_vote_event_chart import RescalingVoteEventChart
from .sad_event_chart import SadEventChart
from .sad_ffmpeg_event_chart import SadFfmpegEventChart
