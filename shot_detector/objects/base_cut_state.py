# -*- coding: utf8 -*-

from __future__ import absolute_import

from .smart_dict import SmartDict

class BaseCutState(SmartDict):
    image           = None
    time            = None
    features        = None
    value           = None
