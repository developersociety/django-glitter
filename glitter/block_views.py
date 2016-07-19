# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template.loader import render_to_string
from glitter.templates import get_layout


def baseblock(block, request, rerender, content_block, block_classes):
    css_classes = ' '.join(block_classes)

    # Find the column
    layout = get_layout(template_name=content_block.obj_version.template_name)
    column = layout._meta.columns[content_block.column]

    return render_to_string((
        'glitter/blocks/%s.html' % (content_block.content_type.model),
        'glitter/blocks/baseblock.html',
    ), {
        'content_block': content_block,
        'css_classes': css_classes,
        'object': block,
        'column': column,
    })
