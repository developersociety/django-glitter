# -*- coding: utf-8 -*-

from django.apps import AppConfig


class PagesConfig(AppConfig):
    name = 'glitter.pages'
    label = 'glitter_pages'
    verbose_name = 'Pages'

    def ready(self):
        super(PagesConfig, self).ready()
        from . import listeners  # noqa
