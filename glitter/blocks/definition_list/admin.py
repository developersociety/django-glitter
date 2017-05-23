# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from glitter.blockadmin import blocks

from .models import DefinitionList, DefinitionListInline


class DefinitionListInlineAdmin(blocks.TabularInline):
    min_num = 1
    extra = 0
    model = DefinitionListInline


class DefinitionListAdmin(blocks.BlockAdmin):
    inlines = [DefinitionListInlineAdmin]


blocks.site.register(DefinitionList, DefinitionListAdmin)
blocks.site.register_block(DefinitionList, 'Common')
