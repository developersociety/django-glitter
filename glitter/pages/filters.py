# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


class GlitterPagePublishedFilter(admin.SimpleListFilter):
    title = 'published'
    parameter_name = 'published'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Yes'),
            ('0', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(published=True).exclude(current_version=None)

        if self.value() == '0':
            return queryset.filter(published=True, current_version__isnull=True)


class GlitterPageLanguageFilter(admin.SimpleListFilter):
    title = 'language'
    parameter_name = 'language'

    def lookups(self, request, model_admin):
        from django.conf import settings
        return settings.PAGE_LANGUAGES

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(language=self.value())
        return queryset
