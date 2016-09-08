# -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def glitter_head(context):
    """
    Template tag which renders the glitter CSS and JavaScript. Any resources
    which need to be loaded should be added here. This is only shown to users
    with permission to edit the page.
    """
    user = context.get('user')
    rendered = ''
    template_path = 'glitter/include/head.html'

    if user is not None and user.is_staff:
        template = context.template.engine.get_template(template_path)
        rendered = template.render(context)

    return rendered


@register.simple_tag(takes_context=True)
def glitter_startbody(context):
    """
    Template tag which renders the glitter overlay and sidebar. This is only
    shown to users with permission to edit the page.
    """
    user = context.get('user')
    path_body = 'glitter/include/startbody.html'
    path_plus = 'glitter/include/startbody_%s_%s.html'
    rendered = ''

    if user is not None and user.is_staff:
        templates = [path_body]
        # We've got a page with a glitter object:
        # - May need a different startbody template
        # - Check if user has permission to add
        glitter = context.get('glitter')
        if glitter is not None:
            opts = glitter.obj._meta.app_label, glitter.obj._meta.model_name
            template_path = path_plus % opts
            templates.insert(0, template_path)
            context['has_add_permission'] = user.has_perm('%s.%s' % opts)

        template = context.template.engine.select_template(templates)
        rendered = template.render(context)

    return rendered


@register.assignment_tag(takes_context=True)
def glitter_columns(context, object):
    """
    Generate a dict of render Glitter Columns for the supplied Glitter Model/Page

    Used for rendering Glitter Model/Pages on non-Glitter pages.

    Example usage:

    {% glitter_columns post as cols %}
    {{ cols.content }}
    """
    glitter_page = Glitter(page_version=object.current_version, request=context.request)
    glitter_columns = glitter_page.render()
    return glitter_columns
