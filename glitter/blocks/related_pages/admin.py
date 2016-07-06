# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from glitter.blockadmin import blocks


from .models import RelatedPage, RelatedPagesBlock


class RelatedPageInline(blocks.StackedInline):
    model = RelatedPage
    extra = 1


class RelatedPagesBlockAdmin(blocks.BlockAdmin):
    inlines = [RelatedPageInline]


blocks.site.register(RelatedPagesBlock, RelatedPagesBlockAdmin)
blocks.site.register_block(RelatedPagesBlock, 'App Blocks')
