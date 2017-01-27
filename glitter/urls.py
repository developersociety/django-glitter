from glitter.pages.models import Page

from django.conf.urls import include, url
from django.db.utils import DatabaseError
from django.core.exceptions import FieldError
from glitter.integration import glitter_app_pool
import importlib

urlpatterns = []

try:
    app_pages = Page.objects.exclude(glitter_app_name='')
    for app_page in app_pages:
        glitter_app = glitter_app_pool.get_glitter_app(app_page.glitter_app_name)
        if glitter_app:
            app_url_conf = importlib.import_module(glitter_app.url_conf)
            importlib.reload(app_url_conf)

            app_url = url(
                '^{}/'.format(app_page.url.strip('/')),
                include(app_url_conf, namespace=glitter_app.namespace)
            )
            urlpatterns.append(app_url)

except DatabaseError:
    # Database not setup correctly, not much we can do
    pass

except FieldError:
    # Likely that migrations to support Glitter Apps have not been executed. Not much we can do.
    pass
