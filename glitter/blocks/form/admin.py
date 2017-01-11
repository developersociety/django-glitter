# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from glitter.blockadmin import blocks

from .models import ContactFormBlock


blocks.site.register(ContactFormBlock)
blocks.site.register_block(ContactFormBlock, 'Forms')
