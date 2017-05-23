# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.forms.widgets import Select

from glitter.blockadmin import blocks
from glitter.widgets import CustomRelatedFieldWidgetWrapper
from .models import Banner, BannerBlock, BannerInline


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass


class BannerInlineAdmin(blocks.StackedInline):
    model = BannerInline
    min_num = 1
    extra = 0

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(BannerInlineAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'banner':
            formfield.widget = CustomRelatedFieldWidgetWrapper(
                widget=Select(),
                rel=db_field.rel,
                admin_site=self.admin_site,
                can_add_related=True,
                can_change_related=True,
            )
        return formfield


class BannerBlockAdmin(blocks.BlockAdmin):
    inlines = [
        BannerInlineAdmin,
    ]


blocks.site.register(BannerBlock, BannerBlockAdmin)
blocks.site.register_block(BannerBlock, 'App Blocks')
