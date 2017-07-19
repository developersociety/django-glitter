# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings

from mptt.forms import MPTTAdminForm

from glitter.integration import glitter_app_pool

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


def get_glitter_app_choices():
    glitter_apps = glitter_app_pool.get_glitter_apps()
    choices = [('', '(none)')]
    for app_system_name, glitter_app in glitter_apps.items():
        choices.append((app_system_name, glitter_app.name))

    # Sort by glitter_app name
    choices = sorted(choices, key=lambda x: x[1])
    return choices


class PageAdminForm(MPTTAdminForm):
    class Meta:
        model = Page
        widgets = {
            'glitter_app_name': forms.widgets.Select(choices=get_glitter_app_choices()),
        }
        fields = '__all__'
