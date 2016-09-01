# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings

from glitter.blockadmin import blocks

from .models import Redactor


class BaseRedactorForm(forms.ModelForm):
    class Meta:
        model = Redactor
        exclude = ()


def redactor_block_form():
    class_choices = getattr(settings, 'GLITTER_REDACTOR_CHOICES', ())

    # No classes? Just return a form without them
    if not class_choices:
        class RedactorForm(BaseRedactorForm):
            class Meta(BaseRedactorForm.Meta):
                exclude = ('block_class',)

        return RedactorForm

    # The more customisable version
    class_required = getattr(settings, 'GLITTER_REDACTOR_REQUIRED', False)

    class RedactorForm(BaseRedactorForm):
        block_class = forms.ChoiceField(
            label='Class', choices=class_choices, required=class_required)

    return RedactorForm


class RedactorAdmin(blocks.BlockAdmin):
    form = redactor_block_form()


blocks.site.register(Redactor, RedactorAdmin)
blocks.site.register_block(Redactor, 'Common')
