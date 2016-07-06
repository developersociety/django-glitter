# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from glitter.blockadmin import blocks

from .forms import LatestTweetsBlockForm
from .models import LatestTweetsBlock


class LatestTweetsBlockAdmin(blocks.BlockAdmin):
    form = LatestTweetsBlockForm


blocks.site.register(LatestTweetsBlock, LatestTweetsBlockAdmin)
blocks.site.register_block(LatestTweetsBlock, 'App Blocks')
