# -*- coding: utf-8 -*-

from django.contrib import admin
from django.forms.widgets import Select

from glitter import block_admin
from glitter.widgets import CustomRelatedFieldWidgetWrapper
from .models import Banner, BannerBlock, BannerInline


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass


class BannerInlineAdmin(block_admin.StackedInline):
    model = BannerInline
    extra = 1

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


class BannerBlockAdmin(block_admin.BlockModelAdmin):
    inlines = [
        BannerInlineAdmin,
    ]


block_admin.site.register(BannerBlock, BannerBlockAdmin)
block_admin.site.register_block(BannerBlock, 'App Blocks')
