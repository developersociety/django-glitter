# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings

from glitter import block_admin

from .models import TextTextBlock


class BaseTextTextBlockForm(forms.ModelForm):
    class Meta:
        model = TextTextBlock
        exclude = ()


def redactor_block_form():
    class_choices = getattr(settings, 'GLITTER_TEXTTEXT_CHOICES', ())

    # No classes? Just return a form without them
    if not class_choices:
        class TextTextBlockForm(BaseTextTextBlockForm):
            class Meta(BaseTextTextBlockForm.Meta):
                exclude = ('block_class',)

        return TextTextBlockForm

    # The more customisable version
    class_required = getattr(settings, 'GLITTER_TEXTTEXT_REQUIRED', False)

    class TextTextBlockForm(BaseTextTextBlockForm):
        block_class = forms.ChoiceField(
            label='Class', choices=class_choices, required=class_required)

    return TextTextBlockForm


class TextTextBlockAdmin(block_admin.BlockModelAdmin):
    form = redactor_block_form()


block_admin.site.register(TextTextBlock, TextTextBlockAdmin)
block_admin.site.register_block(TextTextBlock, 'Common')
