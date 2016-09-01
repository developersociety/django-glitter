# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.utils.encoding import force_text
from django.utils.text import capfirst

from .blockadmin import blocks
from .models import ContentBlock, Version
from .templates import get_layout, get_templates


def get_addblock_form(page_version):
    template_obj = get_layout(template_name=page_version.template_name)

    block_choices = []

    # Group all block by category
    for category in sorted(blocks.site.block_list):
        category_blocks = blocks.site.block_list[category]
        category_choices = (('%s.%s' % (x._meta.app_label, x._meta.object_name),
                             capfirst(force_text(x._meta.verbose_name))) for x in category_blocks)
        category_choices = sorted(category_choices, key=lambda x: x[1])
        block_choices.append((category, category_choices))

    class AddBlockForm(forms.ModelForm):
        class Meta:
            model = ContentBlock
            fields = ('column',)

        block_type = forms.ChoiceField(choices=block_choices)
        column = forms.ChoiceField(
            choices=((x, x) for x in template_obj._meta.columns)
        )
        top = forms.BooleanField(required=False)

    return AddBlockForm


class BaseNewPageTemplateForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ('template_name',)

    template_name = forms.ChoiceField(choices=())


def get_newpagetemplateform(model):
    template_choices = sorted(get_templates(model=model), key=lambda x: x[1])
    initial_template = getattr(settings, 'GLITTER_DEFAULT_TEMPLATE', None)

    class NewPageTemplateForm(BaseNewPageTemplateForm):
        template_name = forms.ChoiceField(choices=template_choices, initial=initial_template)

    return NewPageTemplateForm


class MoveBlockForm(forms.Form):
    MOVE_TOP = 1
    MOVE_UP = 2
    MOVE_DOWN = 3
    MOVE_BOTTOM = 4

    move = forms.IntegerField(min_value=MOVE_TOP, max_value=MOVE_BOTTOM)


def get_movecolumn_form(columns):
    move_choices = ((x, x) for x in columns)

    class MoveColumnForm(forms.Form):
        move = forms.ChoiceField(choices=move_choices)

    return MoveColumnForm
