from django.conf.urls import url

from . import admin

urlpatterns = [
    url(r'^reminders/admin', admin.site.urls),
]
