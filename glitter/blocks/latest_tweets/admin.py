# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from glitter import block_admin

from .forms import LatestTweetsBlockForm
from .models import LatestTweetsBlock


class LatestTweetsBlockAdmin(block_admin.BlockAdmin):
    form = LatestTweetsBlockForm


block_admin.site.register(LatestTweetsBlock, LatestTweetsBlockAdmin)
block_admin.site.register_block(LatestTweetsBlock, 'App Blocks')
