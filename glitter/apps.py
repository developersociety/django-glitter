from django.apps import AppConfig


class GlittersConfig(AppConfig):
    name = 'glitter'
    label = 'glitter'

    def ready(self):
        super().ready()
        self.module.autodiscover()
