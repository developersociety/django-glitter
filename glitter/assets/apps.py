# -*- coding: utf-8 -*-

from django.apps import AppConfig


class GlitterBasicAssetsConfig(AppConfig):
    name = 'glitter.assets'
    label = 'glitter_assets'
    verbose_name = 'Assets'

    def ready(self):
        super(GlitterBasicAssetsConfig, self).ready()
        from . import listeners  # noqa
