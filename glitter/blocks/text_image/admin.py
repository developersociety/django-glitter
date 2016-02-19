# -*- coding: utf-8 -*-

from django.contrib.admin.sites import AdminSite

from glitter import block_admin
from glitter.assets.fields import AssetForeignKey
from glitter.assets.widgets import ImageRelatedFieldWidgetWrapper, ImageSelect

from .forms import BaseTextImageForm
from .models import TextImageBlock


class TextImageBlockAdmin(block_admin.BlockModelAdmin):
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


block_admin.site.register(TextImageBlock, TextImageBlockAdmin)
block_admin.site.register_block(TextImageBlock, 'Common')
