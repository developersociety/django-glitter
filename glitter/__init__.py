# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.module_loading import autodiscover_modules


default_app_config = 'glitter.apps.GlittersConfig'


def autodiscover():
    """ Auto discover for layouts. """
    autodiscover_modules('layouts')
    autodiscover_modules('blocks')
