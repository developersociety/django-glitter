# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from glitter.blockadmin import blocks

from .models import Video


blocks.site.register(Video)
blocks.site.register_block(Video, 'Media')
