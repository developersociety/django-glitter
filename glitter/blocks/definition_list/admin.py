# -*- coding: utf-8 -*-

from glitter import block_admin

from .models import DefinitionList, DefinitionListInline


class DefinitionListInlineAdmin(block_admin.TabularInline):
    model = DefinitionListInline


class DefinitionListAdmin(block_admin.BlockModelAdmin):
    inlines = [DefinitionListInlineAdmin]


block_admin.site.register(DefinitionList, DefinitionListAdmin)
block_admin.site.register_block(DefinitionList, 'Common')
