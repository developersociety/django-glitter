# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings

from .models import Page


class DuplicatePageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['url', 'title', 'parent', 'login_required', 'show_in_navigation']
        labels = {
            'url': 'New URL',
            'title': 'New title',
        }

    def __init__(self, *args, **kwargs):
        if not getattr(settings, 'GLITTER_SHOW_LOGIN_REQUIRED', False):
            if 'login_required' in self.Meta.fields:
                self.Meta.fields.remove('login_required')
        super(DuplicatePageForm, self).__init__(*args, **kwargs)
