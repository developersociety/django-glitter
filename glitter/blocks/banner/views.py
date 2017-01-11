# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template.loader import render_to_string

from glitter.templates import get_layout


def banner_view(block, request, rerender, content_block, block_classes):
    css_classes = ' '.join(block_classes)

    # Find the column
    layout = get_layout(template_name=content_block.obj_version.template_name)
    column = layout._meta.columns[content_block.column]

    banner_inlines = None
    if block:
        banner_inlines = block.bannerinline_set.select_related('banner__image').all()

    template_name = 'glitter/blocks/%s.html' % content_block.content_type.model
    context = {
        'content_block': content_block,
        'css_classes': css_classes,
        'object': block,
        'column': column,
        'banner_inlines': banner_inlines}
    rendered = render_to_string(template_name, context, request=request)
    return rendered
