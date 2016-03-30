from django.template import RequestContext
from django.template.loader import render_to_string
from glitter.templates import get_layout


def banner_view(block, request, rerender, content_block, block_classes):
    css_classes = ' '.join(block_classes)

    # Find the column
    layout = get_layout(template_name=content_block.obj_version.template_name)
    column = layout._meta.columns[content_block.column]

    banner_inlines = block.bannerinline_set.select_related('banner__image').all()

    return render_to_string((
        'glitter/blocks/%s.html' % (block._meta.model_name,),
    ), {
        'content_block': content_block,
        'css_classes': css_classes,
        'object': block,
        'column': column,
        'banner_inlines': banner_inlines,
    }, context_instance=RequestContext(request))
