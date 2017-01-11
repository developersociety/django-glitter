"""
These template tags allows the reusability of django-admin resources between
version 1.8 and 1.8+ of django.
"""
from django import template, VERSION
from django.contrib.staticfiles.templatetags.staticfiles import static
register = template.Library()


@register.simple_tag
def jquery_min():
    "Return the path to jquery.min.js"
    if VERSION >= (1, 9):
        url = static('admin/js/vendor/jquery/jquery.min.js')
    else:
        url = static('admin/js/jquery.min.js')

    return url
