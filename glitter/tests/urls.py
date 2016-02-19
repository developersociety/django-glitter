# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from glitter import block_admin


urlpatterns = [
    # Django admin
    url(r'^admin/', include(admin.site.urls)),

    # Glitter block admin
    url(r'^blockadmin/', include(block_admin.site.urls)),

]
