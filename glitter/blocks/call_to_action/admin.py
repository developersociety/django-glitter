# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from glitter.blockadmin import blocks

from .models import CallToActionBlock


blocks.site.register(CallToActionBlock)
blocks.site.register_block(CallToActionBlock, 'Common')
