# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.forms.widgets import Select

from glitter.blockadmin import blocks

from .models import (
    Carousel, CarouselImage, ImageOnlyCarousel, CarouselBlock, ImageOnlyCarouselBlock,
    ImageOnlyCarouselImage
)
from .widgets import CustomRelatedFieldWidgetWrapper


class CarouselImageInline(admin.StackedInline):
    model = CarouselImage
    extra = 1


class CarouselAdmin(admin.ModelAdmin):
    inlines = [CarouselImageInline]


class CarouselBlockAdmin(blocks.BlockAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(CarouselBlockAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'carousel':
            formfield.widget = CustomRelatedFieldWidgetWrapper(
                widget=Select(),
                rel=db_field.rel,
                admin_site=self.admin_site,
                can_add_related=True,
                can_change_related=True,
            )
        return formfield


class ImageOnlyCarouselImageInline(admin.TabularInline):
    model = ImageOnlyCarouselImage
    extra = 1


class ImageOnlyCarouselAdmin(admin.ModelAdmin):
    inlines = [ImageOnlyCarouselImageInline]


class ImageOnlyCarouselBlockAdmin(blocks.BlockAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(ImageOnlyCarouselBlockAdmin, self).formfield_for_dbfield(
            db_field, **kwargs)
        if db_field.name == 'carousel':
            formfield.widget = CustomRelatedFieldWidgetWrapper(
                widget=Select(),
                rel=db_field.rel,
                admin_site=self.admin_site,
                can_add_related=True,
                can_change_related=True,
            )
        return formfield


admin.site.register(Carousel, CarouselAdmin)
admin.site.register(ImageOnlyCarousel, ImageOnlyCarouselAdmin)

blocks.site.register(CarouselBlock, CarouselBlockAdmin)
blocks.site.register(ImageOnlyCarouselBlock, ImageOnlyCarouselBlockAdmin)

blocks.site.register_block(CarouselBlock, 'Media')
blocks.site.register_block(ImageOnlyCarouselBlock, 'Media')
