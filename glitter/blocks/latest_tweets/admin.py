# -*- coding: utf-8 -*-

from glitter import block_admin

from .forms import LatestTweetsBlockForm
from .models import LatestTweetsBlock


class LatestTweetsBlockAdmin(block_admin.BlockModelAdmin):
    form = LatestTweetsBlockForm


block_admin.site.register(LatestTweetsBlock, LatestTweetsBlockAdmin)
block_admin.site.register_block(LatestTweetsBlock, 'App Blocks')
