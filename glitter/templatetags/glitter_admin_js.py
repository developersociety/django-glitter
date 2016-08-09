"""
These template tags allows the reusability of django-admin resources between
version 1.8 and 1.8+ of django.
"""
from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static
from ..utils import django_version_gt_18
register = template.Library()

@register.simple_tag
def jquery_min():
    "Return the path to jquery.min.js"
    if django_version_gt_18():
        url = static('admin/js/vendor/jquery/jquery.min.js')
    else:
        url = static('admin/js/jquery.min.js')

    return url
        

