# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from glitter import block_admin

from .models import DefinitionList, DefinitionListInline


class DefinitionListInlineAdmin(block_admin.TabularInline):
    model = DefinitionListInline


class DefinitionListAdmin(block_admin.BlockAdmin):
    inlines = [DefinitionListInlineAdmin]


block_admin.site.register(DefinitionList, DefinitionListAdmin)
block_admin.site.register_block(DefinitionList, 'Common')
