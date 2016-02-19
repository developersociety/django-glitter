# -*- coding: utf-8 -*-

from django.db import models

from glitter.assets.fields import AssetForeignKey
from glitter.models import BaseBlock


class BaseImageBlock(BaseBlock):
    image = AssetForeignKey('glitter_assets.Image', null=True, on_delete=models.PROTECT)
    description = models.CharField(max_length=200, blank=True, help_text='Used as ALT text')
    caption = models.CharField(max_length=200, blank=True, help_text='Shown below the image')
    link = models.URLField(blank=True)
    new_window = models.BooleanField('Open link in new window', default=False)

    render_function = 'glitter.blocks.image.views.imageblock'

    class Meta:
        abstract = True


class ImageBlock(BaseImageBlock):
    class Meta:
        verbose_name = 'image'
