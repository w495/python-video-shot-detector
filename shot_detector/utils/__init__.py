# -*- coding: utf8 -*-


"""
    Some utils
"""

from __future__ import absolute_import, division, print_function

from .cli import (
    ColoredHelpFormatter,
    ConfigArgParser
)
from .collections import (
    object_data_dict,
    FrozenDict,
    ReprDict,
    unique

)
from .tex import (
    TexTemplate,
    TeX,
    Qtex,
    Qtext
)
from .iter import handle_content
from .kw_helpers import (
    LazyHelper,
    NotNoneKwDefaultsObject
)
from .log import (
    LogMeta,
    LogSetting
)
