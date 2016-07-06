# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib import admin

from glitter.blockadmin import blocks


urlpatterns = [
    # Django admin
    url(r'^admin/', include(admin.site.urls)),

    # Glitter block admin
    url(r'^blockadmin/', include(blocks.site.urls)),

]
