# -*- coding: utf-8 -*-

from glitter import block_admin

from .models import Video


block_admin.site.register(Video)
block_admin.site.register_block(Video, 'Media')
