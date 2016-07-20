# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin.sites import AdminSite

from glitter.assets.fields import AssetForeignKey
from glitter.assets.widgets import ImageRelatedFieldWidgetWrapper, ImageSelect
from glitter.blockadmin import blocks

from .forms import BaseTextImageForm
from .models import TextImageBlock


class TextImageBlockAdmin(blocks.BlockAdmin):
    form = BaseTextImageForm

    formfield_overrides = {
        AssetForeignKey: {
            'widget': ImageRelatedFieldWidgetWrapper(
                ImageSelect(),
                TextImageBlock._meta.get_field('image').rel,
                AdminSite(),
                can_add_related=True
            )
        }
    }


blocks.site.register(TextImageBlock, TextImageBlockAdmin)
blocks.site.register_block(TextImageBlock, 'Common')
