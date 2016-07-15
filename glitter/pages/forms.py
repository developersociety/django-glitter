# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .models import Page


class DuplicatePageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['url', 'title', 'parent', 'language', 'login_required', 'show_in_navigation']
        labels = {
            'url': 'New URL',
            'title': 'New title',
        }
