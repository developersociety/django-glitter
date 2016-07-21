# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from functools import update_wrapper

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.options import csrf_protect_m
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import MPTTModelAdmin

from glitter.admin import GlitterAdminMixin
from glitter.models import Version

from .filters import GlitterPageLanguageFilter
from .forms import PageAdminForm
from .models import Page


@admin.register(Page)
class PageAdmin(GlitterAdminMixin, DjangoMpttAdmin, MPTTModelAdmin):
    list_display = [
        'title', 'get_url', 'view_url', 'is_published', 'in_nav', 'admin_unpublished_count',
    ]
    mptt_level_indent = 25
    glitter_render = True
    form = PageAdminForm
    change_list_template = 'admin/pages/page/change_list.html'
    change_form_template = 'admin/pages/page/change_form.html'

    def get_fieldsets(self, request, obj=None):
        """ Get the fieldsets for admin. """

        # Check if login required.
        options = ['login_required', 'show_in_navigation']
        if not self.model.is_login_required():
            options.remove('login_required')
        fieldsets = [
            [
                '', {
                    'fields': (
                        'url', 'title', 'parent'
                    )
                }
            ],
            [
                'Options', {
                    'fields': options
                }
            ],
        ]

        # Check if langues required
        if self.model.is_languages_required():
            fieldsets.append([
                'Language', {
                    'fields': (
                        'language',
                    )
                }
            ])
        return fieldsets

    def get_list_display(self, request):
        """ Add languages to the list_display if it's enabled. """

        if self.model.is_languages_required():
            if 'get_language' not in self.list_display:
                self.list_display.append('get_language')
        return self.list_display

    def get_url(self, obj):
        return obj.get_absolute_url()
    get_url.short_description = 'Full URL'

    def get_list_filter(self, request):
        """ Add languages filter if languages is enable. """

        if self.model.is_languages_required():
            if GlitterPageLanguageFilter not in self.list_filter:
                self.list_filter.append(GlitterPageLanguageFilter)
        return self.list_filter

    def view_url(self, obj):
        info = self.model._meta.app_label, self.model._meta.model_name
        redirect_url = reverse('admin:%s_%s_redirect' % info, kwargs={'object_id': obj.id})
        return '<a href="%s">View page</a>' % (redirect_url)
    view_url.short_description = 'View page'
    view_url.allow_tags = True

    def get_language(self, obj):
        return dict(settings.PAGE_LANGUAGES)[obj.language].title()
    get_language.short_description = 'Language'

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
            url(r'^(\d+)/duplicate/$', wrap(self.duplicate_page), name='%s_%s_duplicate' % info),
        ] + urlpatterns
        return urlpatterns

    @csrf_protect_m
    @transaction.atomic
    def duplicate_page(self, request, obj_id):
        obj = get_object_or_404(Page, id=obj_id)

        if not self.has_add_permission(request):
            raise PermissionDenied

        if request.method == "POST":
            form = PageAdminForm(request.POST or None)
            if form.is_valid():
                new_page = form.save()

                # Use current version if exists if not get the latest
                if obj.current_version:
                    current_version = obj.current_version
                else:
                    current_version = obj.get_latest_version()

                if current_version:

                    # Create a new version
                    new_version = Version(content_object=new_page)
                    new_version.template_name = current_version.template_name
                    new_version.version_number = 1
                    new_version.owner = request.user
                    new_version.save()

                    self.duplicate_content(current_version, new_version)

                return HttpResponseRedirect(
                    reverse('admin:glitter_pages_page_change', args=(new_page.id,))
                )
        else:
            form = PageAdminForm(initial={
                'url': obj.url,
                'title': obj.title,
                'parent': obj.parent,
                'language': obj.language,
            })
        fieldsets = self.get_fieldsets(request)
        adminForm = admin.helpers.AdminForm(
            form=form,
            fieldsets=fieldsets,
            prepopulated_fields=self.get_prepopulated_fields(request, obj),
            readonly_fields=self.get_readonly_fields(request, obj),
            model_admin=self
        )
        context = {
            'adminform': adminForm,
            'opts': obj._meta,
            'change': False,
            'is_popup': False,
            'save_as': False,
            'has_delete_permission': self.has_delete_permission(request, obj),
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': self.has_change_permission(request, obj),
        }
        return render(
            request, 'admin/pages/page/duplicate_page.html', context
        )
