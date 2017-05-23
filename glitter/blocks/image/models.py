# -*- coding: utf-8 -*-

from django.db import models

from glitter.assets.fields import AssetForeignKey
from glitter.fields import LinkField
from glitter.models import BaseBlock

from .managers import BaseImageBlockManager


class BaseImageBlock(BaseBlock):
    image = AssetForeignKey('glitter_assets.Image', on_delete=models.PROTECT)
    description = models.CharField(max_length=200, blank=True, help_text='Used as ALT text')
    caption = models.CharField(max_length=200, blank=True, help_text='Shown below the image')
    link = LinkField(blank=True)
    new_window = models.BooleanField('Open link in new window', default=False)

    objects = BaseImageBlockManager()

    class Meta:
        abstract = True


class ImageBlock(BaseImageBlock):
    class Meta:
        verbose_name = 'image'
