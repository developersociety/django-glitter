"""
These template tags allows the reusability of django-admin resources between
version 1.8 and 1.8+ of django.
"""
from django import template, VERSION
from django.contrib.staticfiles.templatetags.staticfiles import static

register = template.Library()

def _version_gt_18():
    "Returns true if version is greater then 1.8"
    is_greater = False

    if VERSION[0] == 1:
        if VERSION[1] > 8:
            is_greater = True
    elif VERSION[0] > 1:
        is_greater = True
    
    return is_greater


@register.simple_tag
def jquery_min():
    "Return the path to jquery.min.js"
    if _version_gt_18():
        url = static('admin/js/vendor/jquery/jquery.min.js')
    else:
        url = static('admin/js/jquery.min.js')

    return url
        

