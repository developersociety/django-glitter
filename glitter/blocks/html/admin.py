# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from glitter.blockadmin import blocks

from .models import HTML


blocks.site.register(HTML)
blocks.site.register_block(HTML, 'Common')
