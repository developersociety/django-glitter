# -*- coding: utf-8 -*-

from django.apps import AppConfig


class GlittersConfig(AppConfig):
    name = 'glitter'
    label = 'glitter'

    def ready(self):
        super(GlittersConfig, self).ready()
        self.module.autodiscover()
