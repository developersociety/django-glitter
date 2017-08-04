from django.apps import AppConfig


class PagesConfig(AppConfig):
    name = 'glitter.pages'
    label = 'glitter_pages'
    verbose_name = 'Pages'

    def ready(self):
        super().ready()
        from . import listeners  # noqa
