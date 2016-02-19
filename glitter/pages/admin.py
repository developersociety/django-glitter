# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from functools import update_wrapper

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.options import csrf_protect_m
from django.core.urlresolvers import reverse

from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import MPTTModelAdmin

from glitter.admin import GlitterAdminMixin
from .models import Page


def page_admin_fields():
    fields = ['url', 'title', 'parent', 'login_required', 'show_in_navigation']

    # Don't show login_required unless needed
    if not getattr(settings, 'GLITTER_SHOW_LOGIN_REQUIRED', False):
        fields.remove('login_required')

    return fields


@admin.register(Page)
class PageAdmin(GlitterAdminMixin, DjangoMpttAdmin, MPTTModelAdmin):
    list_display = (
        'title', 'url', 'view_url', 'is_published', 'in_nav', 'admin_unpublished_count',
    )
    fields = page_admin_fields()
    mptt_level_indent = 25
    glitter_render = True
    change_list_template = 'admin/pages/page/change_list.html'

    def view_url(self, obj):
        info = self.model._meta.app_label, self.model._meta.model_name
        redirect_url = reverse('admin:%s_%s_redirect' % info, kwargs={'object_id': obj.id})
        return '<a href="%s">View page</a>' % (redirect_url)
    view_url.short_description = 'View page'
    view_url.allow_tags = True

    def in_nav(self, obj):
        return obj.show_in_navigation
    in_nav.boolean = True

    def admin_unpublished_count(self, obj):
        return obj.unpublished_count or ''
    admin_unpublished_count.short_description = 'Unpublished pages'
    admin_unpublished_count.allow_tags = True

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        template_response = super(PageAdmin, self).changelist_view(request, extra_context)
        template_response.template_name = 'admin/pages/page/change_list_tree.html'
        return template_response

    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        urlpatterns = super(PageAdmin, self).get_urls()

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            url(r'^$', wrap(self.grid_view)),
            url(r'^tree/$', wrap(self.changelist_view), name='%s_%s_tree' % info),
        ] + urlpatterns
        return urlpatterns
