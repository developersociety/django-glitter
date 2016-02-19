from django import template
from django.contrib.admin.templatetags.admin_modify import submit_row

register = template.Library()


@register.inclusion_tag('admin/glitter/page/submit_line.html', takes_context=True)
def glitter_submit_row(context):
    return submit_row(context)
