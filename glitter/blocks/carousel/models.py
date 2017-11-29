# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from glitter.assets.fields import AssetForeignKey
from glitter.fields import LinkField
from glitter.models import BaseBlock


@python_2_unicode_compatible
class BaseCarousel(models.Model):
    title = models.CharField(max_length=100, db_index=True)

    class Meta:
        abstract = True
        ordering = ('title',)

    def __str__(self):
        return self.title


class Carousel(BaseCarousel):
    pass


@python_2_unicode_compatible
class BaseCarouselImage(models.Model):
    carousel = models.ForeignKey(Carousel, related_name='carousel_images')
    title = models.CharField(max_length=100)
    subtitle = models.TextField(blank=True)
    image = AssetForeignKey('glitter_assets.Image', on_delete=models.PROTECT)
    link = LinkField()
    position = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ('position', 'id')
        abstract = True

    def __str__(self):
        return self.title


class CarouselImage(BaseCarouselImage):
    pass


class CarouselBlock(BaseBlock):
    carousel = models.ForeignKey(Carousel, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'carousel'


class ImageOnlyCarousel(BaseCarousel):
    pass


@python_2_unicode_compatible
class BaseImageOnlyCarouselImage(models.Model):
    carousel = models.ForeignKey(ImageOnlyCarousel, related_name='carousel_images')
    image = AssetForeignKey('glitter_assets.Image', on_delete=models.PROTECT)
    position = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ('position', 'id')
        abstract = True

    def __str__(self):
        if self.carousel:
            return '{}'.format(self.carousel)
        else:
            return 'Carousel image'


class ImageOnlyCarouselImage(BaseImageOnlyCarouselImage):
    pass


class ImageOnlyCarouselBlock(BaseBlock):
    carousel = models.ForeignKey(ImageOnlyCarousel, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'image only carousel'
