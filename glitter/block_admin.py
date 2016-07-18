# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import warnings

from glitter.blockadmin.blocks import BlockAdmin, site, StackedInline, TabularInline

from .models import BaseBlock  # noqa


BlockModelAdmin = BlockAdmin

__all__ = ['site', 'BlockModelAdmin', 'StackedInline', 'TabularInline']


warnings.warn(
    "BlockModelAdmin has been moved to blockadmin.blocks.BlockAdmin",
    DeprecationWarning,
    stacklevel=2
)
