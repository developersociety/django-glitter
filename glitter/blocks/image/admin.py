# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from glitter import block_admin
from glitter.assets.models import Image
from glitter.assets.widgets import ImageRelatedFieldWidgetWrapper, ImageSelect

from django.conf.urls import url
from django.http import JsonResponse
from django.template import Context
from django.template.loader import get_template

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
        last_image_id = request.GET['last_image_id']
        images = Image.objects.filter(
            id__lt=last_image_id
        ).order_by(
            '-created_at', 'modified_at', 'title'
        )[:20]
        template = get_template('glitter/blocks/includes/lazy_images.html')
        context = Context({'images': images})
        html = template.render(context)
        return JsonResponse({'html': html, 'last_image_id': last_image_id})


block_admin.site.register(ImageBlock, ImageBlockAdmin)
block_admin.site.register_block(ImageBlock, 'Common')
