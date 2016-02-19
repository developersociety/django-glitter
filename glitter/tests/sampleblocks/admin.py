# -*- coding: utf-8 -*-

from glitter import block_admin

from .models import SampleModelWithInlinesBlock, SampleInline


class SampleInlineAdmin(block_admin.StackedInline):
    model = SampleInline


class SampleModelWithInlinesBlockAdmin(block_admin.BlockModelAdmin):
    inlines = [SampleInlineAdmin]


block_admin.site.register(SampleModelWithInlinesBlock, SampleModelWithInlinesBlockAdmin)
block_admin.site.register_block(SampleModelWithInlinesBlock, 'Sample Blocks')
