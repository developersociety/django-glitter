# -*- coding: utf-8 -*-

from django.template.loader import render_to_string


def baseblock(block, request, rerender, content_block, block_classes):
    css_classes = ' '.join(block_classes)

    return render_to_string((
        'glitter/blocks/%s.html' % (block._meta.model_name,),
        'glitter/blocks/baseblock.html',
    ), {
        'content_block': content_block,
        'css_classes': css_classes,
        'object': block,
    })
