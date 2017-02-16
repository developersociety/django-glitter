from django.conf import settings
from importlib import import_module


class GlitterApp(object):
    """
    A simple class to store Glitter App config options.
    """
    def __init__(self, name, url_conf, namespace=None):
        self.name = name
        self.url_conf = url_conf
        self.namespace = namespace

    def __str__(self):
        return self.name


class GlitterAppPool(object):
    """
    An interface to the Glitter App configs in the current project.

    Will lazily discover Glitter App configs when needed.
    """
    def __init__(self):
        self.glitter_apps = {}
        self.discovered = False

    def get_glitter_app(self, glitter_app_name):
        """
        Retrieve the Glitter App config for a specific Glitter App.
        """
        if not self.discovered:
            self.discover_glitter_apps()

        try:
            glitter_app = self.glitter_apps[glitter_app_name]
            return glitter_app
        except KeyError:
            return None

    def discover_glitter_apps(self):
        """
        Find all the Glitter App configurations in the current project.
        """
        for app_name in settings.INSTALLED_APPS:
            module_name = '{app_name}.glitter_apps'.format(app_name=app_name)
            try:
                glitter_apps_module = import_module(module_name)
                if hasattr(glitter_apps_module, 'apps'):
                    self.glitter_apps.update(glitter_apps_module.apps)
            except ImportError:
                pass

        self.discovered = True

    def get_glitter_apps(self):
        if not self.discovered:
            self.discover_glitter_apps()
        return self.glitter_apps


glitter_app_pool = GlitterAppPool()
