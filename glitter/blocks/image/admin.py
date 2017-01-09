# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from glitter import block_admin
from glitter.assets.widgets import ImageRelatedFieldWidgetWrapper, ImageSelect

from django.conf.urls import url

from .forms import ImageBlockForm
from .models import ImageBlock


class ImageBlockAdmin(block_admin.BlockModelAdmin):
    form = ImageBlockForm

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Hook for specifying the form Field instance for a given database Field
        instance.

        If kwargs are given, they're passed to the form Field's constructor.
        """
        formfield = super(ImageBlockAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'image':
            formfield.widget = ImageRelatedFieldWidgetWrapper(
                ImageSelect(), db_field.rel, self.admin_site, can_add_related=True,
                can_change_related=True,
            )
        return formfield

    def get_urls(self):
        urls = super(ImageBlockAdmin, self).get_urls()
        image_block_urls = [
            url(r'^get-lazy-images/$', self.get_lazy_images, name='get-lazy-images')
        ]
        return image_block_urls + urls

    def get_lazy_images(self, request):
        import ipdb; ipdb.set_trace()

block_admin.site.register(ImageBlock, ImageBlockAdmin)
block_admin.site.register_block(ImageBlock, 'Common')
