from django.apps import AppConfig


class GlitterBasicAssetsConfig(AppConfig):
    name = 'glitter.assets'
    label = 'glitter_assets'
    verbose_name = 'Assets'

    def ready(self):
        super().ready()
        from . import listeners  # noqa
