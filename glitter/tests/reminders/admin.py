from django.contrib import admin

from glitter.pages.admin import PageAdmin
from glitter.pages.models import Page

site = admin.AdminSite(name='admin')

site.register(Page, PageAdmin)
