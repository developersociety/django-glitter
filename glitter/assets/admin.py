# -*- coding: utf-8 -*-

from os.path import basename

from django.contrib import admin

from .models import ImageCategory, Image, FileCategory, File


@admin.register(ImageCategory, FileCategory)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)


@admin.register(Image, File)
class FileAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('title', 'category', 'file_link', 'modified_at', 'created_at',)
    list_filter = ('category',)
    search_fields = ('title',)
    readonly_fields = ('modified_at', 'created_at',)

    def file_link(self, obj):
        return '<a href="%s">%s</a>' % (obj.get_absolute_url(), basename(obj.file.name))
    file_link.short_description = 'Link'
    file_link.allow_tags = True
