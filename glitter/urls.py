from glitter.pages.models import Page

from django.conf.urls import include, url
from django.db.utils import DatabaseError
from django.core.exceptions import FieldError
from glitter.integration import glitter_app_pool
import importlib

urlpatterns = []
used_apps = []

try:
    # Attempt to find all Glitter App Pages, get their corresponding Glitter App configs and then
    # use those to create URL patterns.
    app_pages = Page.objects.exclude(glitter_app_name='')
    for app_page in app_pages:
        glitter_app = glitter_app_pool.get_glitter_app(app_page.glitter_app_name)
        if glitter_app:
            app_url_conf = importlib.import_module(glitter_app.url_conf)

            # Django caches URLs quite hard, without the reload it continues to just use the
            # cached version.
            importlib.reload(app_url_conf)

            app_url = url(
                '^{}/'.format(app_page.url.strip('/')),
                include(app_url_conf, namespace=glitter_app.namespace)
            )
            urlpatterns.append(app_url)
            used_apps.append(app_page.glitter_app_name)

    # If a page has not been created for an app yet, we don't want a NoReverseMatch error every
    # time someone tries to '{% url %}' or 'reverse()' a viewname. So lets add a URL pattern entry
    # to support those requests.
    glitter_apps = glitter_app_pool.get_glitter_apps()
    for system_name, glitter_app in glitter_apps.items():
        if system_name not in used_apps:
            app_url_conf = importlib.import_module(glitter_app.url_conf)

            app_url = url(
                '^{}/'.format(system_name),
                include(app_url_conf, namespace=glitter_app.namespace)
            )
            urlpatterns.append(app_url)

except DatabaseError:
    # Database not setup correctly, not much we can do
    pass

except FieldError:
    # Likely that migrations to support Glitter Apps have not been executed. Not much we can do.
    pass
