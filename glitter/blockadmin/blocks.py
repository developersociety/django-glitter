# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import update_wrapper

from django.conf import settings
from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.utils import unquote, quote
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import resolve, reverse
from django.db.models.base import ModelBase
from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.template.response import TemplateResponse
from django.utils import six
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from glitter.models import ContentBlock, Version
from glitter.page import Glitter
from glitter.templates import get_layout
from glitter.utils import JSONEncoderForHTML


class BlockAdminSite(AdminSite):
    change_form_template = 'blockadmin/change_form.html'

    def __init__(self, *args, **kwargs):
        # All blocks can be registered to this admin site
        self.block_list = {}

        super(BlockAdminSite, self).__init__(*args, **kwargs)

    # Use the block admin class by default
    def register(self, model_or_iterable, admin_class=None, **options):
        if not admin_class:
            admin_class = BlockAdmin

        category = options.pop('category', None)
        if category:
            self.register_block(model_or_iterable, category)

        super(BlockAdminSite, self).register(model_or_iterable, admin_class, **options)

    # Blocks from the site or other apps can be registered
    def register_block(self, block_or_iterable, category):
        if category not in self.block_list:
            self.block_list[category] = []

        if issubclass(block_or_iterable.__class__, ModelBase):
            self.block_list[category].append(block_or_iterable)
        else:
            for block in block_or_iterable:
                self.block_list[category].append(block)

    def unregister_block(self, block, category):
        try:
            self.block_list[category].remove(block)
        except ValueError:
            pass

    # Remove all of the default admin URLs, we only want the model views for
    # the block admin.
    def get_urls(self):
        from django.conf.urls import url, include

        if settings.DEBUG:
            self.check_dependencies()

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        # Admin-site-wide views.
        urlpatterns = [
            url(r'^jsi18n/$', wrap(self.i18n_javascript, cacheable=True), name='jsi18n'),
        ]

        # Add in each model's views.
        for model, model_admin in six.iteritems(self._registry):
            urlpatterns += [
                url(r'^%s/%s/' % (model._meta.app_label, model._meta.model_name),
                    include(model_admin.urls))
            ]
        return urlpatterns

    # We have no logout here, so just raise PermissionDenied if needed
    def admin_view(self, view, cacheable=False):
        def inner(request, *args, **kwargs):
            if not self.has_permission(request):
                raise PermissionDenied
            return view(request, *args, **kwargs)
        if not cacheable:
            inner = never_cache(inner)
        # We add csrf_protect here so this function can be used as a utility
        # function for any view, without having to repeat 'csrf_protect'.
        inner = csrf_protect(inner)
        return update_wrapper(inner, view)

    def get_app_list(self, request):
        return {}


class BlockAdmin(ModelAdmin):
    # Keep block admin change forms in the blockadmin template directory
    @property
    def change_form_template(self):
        opts = self.model._meta
        app_label = opts.app_label

        return (
            "blockadmin/%s/%s/change_form.html" % (app_label, opts.object_name.lower()),
            "blockadmin/%s/change_form.html" % app_label,
            "blockadmin/change_form.html"
        )

    # We only want the change form for the block admin
    def get_urls(self):
        from django.conf.urls import url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            url(r'^add/(?P<version_id>\d+)/$', wrap(self.add_view), name='%s_%s_add' % info),
            url(r'^(.+)/continue/$', wrap(self.continue_view), name='%s_%s_continue' % info),
            url(r'^(.+)/$', wrap(self.change_view), name='%s_%s_change' % info),
        ]
        return urlpatterns

    def log_change(self, request, object, message):
        pass

    def response_rerender(self, request, obj, template, extra_context=None):
        request.current_app = self.admin_site.name
        content_block = obj.content_block
        version = content_block.obj_version

        glitter = Glitter(version, request=request)
        columns = glitter.render(edit_mode=True, rerender=True)

        context = {
            'column': slugify(content_block.column),
            'rendered_json': JSONEncoderForHTML().encode({
                'content': columns[content_block.column],
            }),
        }

        if extra_context is not None:
            context.update(extra_context)

        return TemplateResponse(request, template, context)

    # A redirect back to the edit view
    def continue_view(self, request, object_id):
        obj = self.get_object(request, unquote(object_id))

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                'name': force_text(self.opts.verbose_name),
                'key': escape(object_id)},
            )

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        opts = self.opts.app_label, self.opts.model_name
        change_url = reverse(
            'admin:%s_%s_change' % opts,
            args=(object_id,),
            current_app=self.admin_site.name)

        # This template will rerender the
        return self.response_rerender(request, obj, 'blockadmin/continue.html', {
            'change_url': change_url,
        })

    def get_version(self, request):
        # As this is the Django admin and we can't just set self.version_id due to thread safety
        # issues, we need to find the version ID of the page when adding a new block. It'll be
        # accessible in the URL - although this is a very hacky way to access it.
        func, args, kwargs = resolve(request.path)
        version_id = kwargs.get('version_id', None)

        if version_id is None:
            # If a version_id kwarg isn't given - we're probably being called by change_view, so
            # there isn't a Version for this request
            return None
        else:
            return Version.objects.get(id=version_id)

    def has_glitter_edit_permission(self, request, obj):
        """
        Return a boolean if a user has edit access to the glitter object/page this object is on.
        """

        # We're testing for the edit permission here with the glitter object - not the current
        # object, not the change permission. Once a user has edit access to an object they can edit
        # all content on it.
        permission_name = '{}.edit_{}'.format(
            obj._meta.app_label, obj._meta.model_name,
        )
        has_permission = (
            request.user.has_perm(permission_name) or
            request.user.has_perm(permission_name, obj=obj)
        )
        return has_permission

    def has_add_permission(self, request):
        # Find the glitter object to see if they've got permission to edit that
        version = self.get_version(request=request)

        # If a version can't be found for this request, it's probably being called by change_view.
        # In this case we just return True as it shouldn't matter.
        if version is None:
            return True

        glitter_obj = version.content_object

        # Use the glitter object for permission testing
        has_permission = self.has_glitter_edit_permission(request, obj=glitter_obj)
        return has_permission

    def has_change_permission(self, request, obj=None):
        # This shouldn't happen - but given that we need to find out the permissions for the
        # glitter object and not just this content block, just fail early incase something goes
        # wrong.
        if obj is None:
            return False

        # Find the glitter object to see if they've got permission to edit that
        version = obj.content_block.obj_version
        glitter_obj = version.content_object

        # Use the glitter object for permission testing
        has_permission = self.has_glitter_edit_permission(request, obj=glitter_obj)
        return has_permission

    def add_view(self, request, version_id, form_url='', extra_context=None):
        version = get_object_or_404(Version, id=version_id)

        # Version must not be saved, and must belong to this user
        if version.version_number or version.owner != request.user:
            raise PermissionDenied

        # Need to ensure that new blocks go into valid columns
        template_obj = get_layout(template_name=version.template_name)
        column_choices = list(template_obj._meta.columns)

        if request.GET.get('column') not in column_choices:
            return HttpResponseBadRequest('Invalid column')

        return self.changeform_view(request, None, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """The 'change' admin view for this model."""

        obj = self.get_object(request, unquote(object_id))

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                'name': force_text(self.opts.verbose_name),
                'key': escape(object_id),
            })

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        content_block = obj.content_block
        version = content_block.obj_version

        # Version must not be saved, and must belong to this user
        if version.version_number or version.owner != request.user:
            raise PermissionDenied

        return super(BlockAdmin, self).change_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        """Determine the HttpResponse for the change_view stage."""
        opts = self.opts.app_label, self.opts.model_name
        pk_value = obj._get_pk_val()

        if '_continue' in request.POST:
            msg = _(
                'The %(name)s block was changed successfully. You may edit it again below.'
            ) % {'name': force_text(self.opts.verbose_name)}

            self.message_user(request, msg, messages.SUCCESS)

            # We redirect to the save and continue page, which updates the
            # parent window in javascript and redirects back to the edit page
            # in javascript.
            return HttpResponseRedirect(reverse(
                'admin:%s_%s_continue' % opts,
                args=(pk_value,),
                current_app=self.admin_site.name
            ))

        # Update column and close popup - don't bother with a message as they won't see it
        return self.response_rerender(request, obj, 'admin/glitter/update_column.html')

    def save_model(self, request, obj, form, change):
        super(BlockAdmin, self).save_model(request, obj, form, change)

        # Whenever we're adding a new block to a page, we'll need to create a ContentBlock to go
        # along with it
        if change is False:
            version = self.get_version(request=request)

            # Create a content block to link the version and the block
            content_block = ContentBlock(
                obj_version=version,
                column=request.GET['column'],
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id,
            )

            if request.GET.get('top', '').lower() == 'true':
                # User wants block at the top of the column, so set the position or it'll end up
                # being autosaved to the end of the column
                first_block = ContentBlock.objects.filter(
                    obj_version=version, column=content_block.column,
                ).first()

                if first_block is not None:
                    content_block.position = first_block.position - 1

            content_block.save()

            obj.content_block = content_block
            obj.save(update_fields=['content_block'])

    def response_add(self, request, obj, post_url_continue=None):
        opts = obj._meta
        pk_value = obj._get_pk_val()

        # Save and continue editing - continue with the iframe
        if '_continue' in request.POST:
            msg = _('The block was added successfully. You may edit it again below.')
            self.message_user(request, msg, messages.SUCCESS)

            # We redirect to the save and continue page, which updates the
            # parent window in javascript and redirects back to the edit page
            # in javascript.
            post_url_continue = reverse(
                'block_admin:%s_%s_continue' % (opts.app_label, opts.model_name),
                args=(quote(pk_value),),
                current_app=self.admin_site.name
            )
            return HttpResponseRedirect(post_url_continue)

        # Update column and close popup - don't bother with a message as they won't see it
        return self.response_rerender(request, obj, 'admin/glitter/update_column.html')


class InlineBlockAdmin(InlineModelAdmin):
    # For inline objects we always allow adding/editing/deleting. This is an additional check done
    # after the permissions for the object has been checked - everyone needs to be able to edit the
    # same content on the same page, so just allow all inlines.

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class StackedInline(InlineBlockAdmin):
    template = 'admin/edit_inline/stacked.html'


class TabularInline(InlineBlockAdmin):
    template = 'admin/edit_inline/tabular.html'

site = BlockAdminSite(name='block_admin')


def register(model, admin=None, category=None):
    """ Decorator to registering you Admin class. """
    def _model_admin_wrapper(admin_class):

        site.register(model, admin_class=admin_class)

        if category:
            site.register_block(model, category)

        return admin_class
    return _model_admin_wrapper
