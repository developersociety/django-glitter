# -*- coding: utf-8 -*-

from django import template
from django.template.loader import get_template, select_template

register = template.Library()


@register.simple_tag(takes_context=True)
def glitter_head(context):
    """
    Template tag which renders the glitter CSS and JavaScript. Any resources
    which need to be loaded should be added here. This is only shown to users
    with permission to edit the page.
    """
    user = context.get('user')

    if user is not None and user.is_staff:
        template = get_template('glitter/include/head.html')
        return template.render(context)
    return ''


@register.simple_tag(takes_context=True)
def glitter_startbody(context):
    """
    Template tag which renders the glitter overlay and sidebar. This is only
    shown to users with permission to edit the page.
    """
    user = context.get('user')

    if user is not None and user.is_staff:
        template_list = ['glitter/include/startbody.html']

        # We've got a page with a glitter object:
        # - May need a different startbody template
        # - Check if user has permission to add
        glitter = context.get('glitter')
        if glitter is not None:
            opts = glitter.obj._meta.app_label, glitter.obj._meta.model_name
            template_list = [
                'glitter/include/startbody_%s_%s.html' % opts] + template_list

            context['has_add_permission'] = user.has_perm('%s.%s' % opts)

        template = select_template(template_list)
        return template.render(context)
    return ''
