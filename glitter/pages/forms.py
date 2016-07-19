# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings

from .models import Page


class DuplicatePageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['url', 'title', 'parent', 'language', 'login_required', 'show_in_navigation']
        labels = {
            'url': 'New URL',
            'title': 'New title',
        }

    def __init__(self, *args, **kwargs):
        super(DuplicatePageForm, self).__init__(*args, **kwargs)
        if hasattr(settings, 'PAGE_LANGUAGES'):
            self.fields['language'].widget = forms.widgets.Select(
                choices=settings.PAGE_LANGUAGES
            )


class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = [
            'url', 'title', 'parent', 'language', 'login_required', 'show_in_navigation'
        ]

    def __init__(self, *args, **kwargs):
        super(PageAdminForm, self).__init__(*args, **kwargs)
        if hasattr(settings, 'PAGE_LANGUAGES'):
            self.fields['language'].widget = forms.widgets.Select(
                choices=settings.PAGE_LANGUAGES
            )
