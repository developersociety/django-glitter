# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings

from glitter import block_admin
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


class RedactorAdmin(block_admin.BlockModelAdmin):
    form = redactor_block_form()


block_admin.site.register(Redactor, RedactorAdmin)
block_admin.site.register_block(Redactor, 'Common')
