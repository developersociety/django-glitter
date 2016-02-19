from django.template import RequestContext
from django.template.loader import render_to_string


def banner_view(block, request, rerender, content_block, block_classes):
    css_classes = ' '.join(block_classes)

    banner_inlines = block.bannerinline_set.select_related('banner__image').all()

    return render_to_string((
        'glitter/blocks/%s.html' % (block._meta.model_name,),
    ), {
        'content_block': content_block,
        'css_classes': css_classes,
        'object': block,
        'banner_inlines': banner_inlines,
    }, context_instance=RequestContext(request))
