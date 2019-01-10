# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from glitter.assets.fields import AssetForeignKey
from glitter.models import BaseBlock


class BaseTextImageBlock(BaseBlock):
    position = models.CharField(max_length=50)
    image = AssetForeignKey('glitter_assets.Image', null=True, on_delete=models.PROTECT)
    content = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        if self.content_block:
            return str(self.content_block)


class TextImageBlock(BaseTextImageBlock):
    class Meta:
        verbose_name = 'Text/Image'
