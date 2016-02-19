# -*- coding: utf-8 -*-

from glitter.templates import get_layout
from django.template.loader import render_to_string

from sorl.thumbnail import get_thumbnail


def imageblock(block, request, rerender, content_block, block_classes):
    css_classes = ' '.join(block_classes)

    thumb = None

    if block.image:
        # Get the block width from the layout
        layout = get_layout(template_name=content_block.obj_version.template_name)
        block_column = layout._meta.columns[content_block.column]

        image = block.image

        # Resize!
        thumb = get_thumbnail(image.file, '%d' % (block_column.width,))

    return render_to_string('glitter/blocks/%s.html' % (block._meta.model_name,), {
        'content_block': content_block,
        'css_classes': css_classes,
        'object': block,
        'thumb': thumb,
    })
