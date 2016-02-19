# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings

from .choices import POSITION_CHOICES
from .models import BaseTextImageBlock


class BaseTextImageForm(forms.ModelForm):
    class Meta:
        model = BaseTextImageBlock
        fields = ('position', 'image', 'content')

    position = forms.ChoiceField(
        choices=getattr(settings, 'GLITTER_TEXTIMAGE_CHOICES', POSITION_CHOICES))
