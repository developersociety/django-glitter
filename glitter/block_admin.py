# -*- coding: utf-8 -*-

import copy
from functools import update_wrapper

from django.conf import settings
from django.contrib import messages
from django.contrib.admin import ModelAdmin, site as admin_site, widgets
from django.contrib.admin.options import get_ul_class, InlineModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.utils import unquote
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple, SelectMultiple
from django.http import Http404, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.template.response import TemplateResponse
from django.utils import six
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.translation import string_concat, ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from .page import Glitter
from .utils import JSONEncoderForHTML


class BlockAdminSite(AdminSite):
    change_form_template = 'blockadmin/change_form.html'

    def __init__(self, *args, **kwargs):
        # All blocks can be registered to this admin site
        self.block_list = {}

        super(BlockAdminSite, self).__init__(*args, **kwargs)

    # Use the block admin class by default
    def register(self, model_or_iterable, admin_class=None, **options):
        if not admin_class:
            admin_class = BlockModelAdmin

        super(BlockAdminSite, self).register(model_or_iterable, admin_class, **options)

    # Blocks from the site or other apps can be registered
    def register_block(self, block, category):
        if category not in self.block_list:
            self.block_list[category] = []

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


class BlockModelAdmin(ModelAdmin):
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
            url(r'^(.+)/continue/$',
                wrap(self.continue_view),
                name='%s_%s_continue' % info),
            url(r'^(.+)/$',
                wrap(self.change_view),
                name='%s_%s_change' % info),
        ]
        return urlpatterns

    def log_change(self, request, object, message):
        pass

    def response_rerender(self, request, obj, template, extra_context=None):
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

        return TemplateResponse(request, template, context, current_app=self.admin_site.name)

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

    def has_change_permission(self, request, obj=None):
        # This shouldn't happen - but given that we need to find out the permissions for the glitter
        # object and not just this content block, just fail early incase something goes wrong.
        if obj is None:
            return False

        # Find the glitter object to see if they've got permission to edit that
        version = obj.content_block.obj_version
        glitter_obj = version.content_object
        opts = glitter_obj._meta.app_label, glitter_obj._meta.model_name
        return request.user.has_perm('%s.edit_%s' % opts)

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

        return super(BlockModelAdmin, self).change_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        """Determine the HttpResponse for the change_view stage."""
        opts = self.opts.app_label, self.opts.model_name
        pk_value = obj._get_pk_val()

        if "_continue" in request.POST:
            msg = _('The %(name)s block was changed successfully. You may edit it again below.') % {
                'name': force_text(self.opts.verbose_name),
            }
            self.message_user(request, msg, messages.SUCCESS)

            # We redirect to the save and continue page, which updates the
            # parent window in javascript and redirects back to the edit page
            # in javascript.
            return HttpResponseRedirect(reverse(
                'admin:%s_%s_continue' % opts,
                args=(pk_value,),
                current_app=self.admin_site.name))

        # Update column and close popup - don't bother with a message as they won't see it
        return self.response_rerender(request, obj, 'admin/glitter/update_column.html')

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Hook for specifying the form Field instance for a given database Field
        instance.
        If kwargs are given, they're passed to the form Field's constructor.
        """
        request = kwargs.pop("request", None)

        # If the field specifies choices, we don't need to look for special
        # admin widgets - we just need to use a select widget of some kind.
        if db_field.choices:
            return self.formfield_for_choice_field(db_field, request, **kwargs)

        # ForeignKey or ManyToManyFields
        if isinstance(db_field, (models.ForeignKey, models.ManyToManyField)):
            # Combine the field kwargs with any options for formfield_overrides.
            # Make sure the passed in **kwargs override anything in
            # formfield_overrides because **kwargs is more specific, and should
            # always win.
            if db_field.__class__ in self.formfield_overrides:
                kwargs = dict(self.formfield_overrides[db_field.__class__], **kwargs)

            # Get the correct formfield.
            if isinstance(db_field, models.ForeignKey):
                formfield = self.formfield_for_foreignkey(db_field, request, **kwargs)
            elif isinstance(db_field, models.ManyToManyField):
                formfield = self.formfield_for_manytomany(db_field, request, **kwargs)

            # For non-raw_id fields, wrap the widget with a wrapper that adds
            # extra HTML -- the "add other" interface -- to the end of the
            # rendered output. formfield can be None if it came from a
            # OneToOneField with parent_link=True or a M2M intermediary.
            if formfield and db_field.name not in self.raw_id_fields:
                related_modeladmin = admin_site._registry.get(db_field.rel.to)
                wrapper_kwargs = {}
                if related_modeladmin:
                    wrapper_kwargs.update(
                        can_add_related=related_modeladmin.has_add_permission(request),
                        can_change_related=related_modeladmin.has_change_permission(request),
                        can_delete_related=related_modeladmin.has_delete_permission(request),
                    )
                formfield.widget = widgets.RelatedFieldWidgetWrapper(
                    formfield.widget, db_field.rel, admin_site, **wrapper_kwargs
                )

            return formfield

        return super(BlockModelAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a ForeignKey.
        """
        db = kwargs.get('using')
        if db_field.name in self.raw_id_fields:
            kwargs['widget'] = widgets.ForeignKeyRawIdWidget(db_field.rel, admin_site, using=db)
        elif db_field.name in self.radio_fields:
            kwargs['widget'] = widgets.AdminRadioSelect(attrs={
                'class': get_ul_class(self.radio_fields[db_field.name]),
            })
            kwargs['empty_label'] = _('None') if db_field.blank else None

        if 'queryset' not in kwargs:
            queryset = self.get_field_queryset(db, db_field, request)
            if queryset is not None:
                kwargs['queryset'] = queryset

        return db_field.formfield(**kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a ManyToManyField.
        """
        # If it uses an intermediary model that isn't auto created, don't show
        # a field in admin.
        if not db_field.rel.through._meta.auto_created:
            return None
        db = kwargs.get('using')

        if db_field.name in self.raw_id_fields:
            kwargs['widget'] = widgets.ManyToManyRawIdWidget(db_field.rel, admin_site, using=db)
            kwargs['help_text'] = ''
        elif db_field.name in (list(self.filter_vertical) + list(self.filter_horizontal)):
            kwargs['widget'] = widgets.FilteredSelectMultiple(
                db_field.verbose_name,
                db_field.name in self.filter_vertical
            )

        if 'queryset' not in kwargs:
            queryset = self.get_field_queryset(db, db_field, request)
            if queryset is not None:
                kwargs['queryset'] = queryset

        form_field = db_field.formfield(**kwargs)
        if isinstance(form_field.widget, SelectMultiple) and not isinstance(form_field.widget, CheckboxSelectMultiple):
            msg = _('Hold down "Control", or "Command" on a Mac, to select more than one.')
            help_text = form_field.help_text
            form_field.help_text = string_concat(help_text, ' ', msg) if help_text else msg
        return form_field


class InlineBlockModelAdmin(InlineModelAdmin):
    # For inline objects we always allow adding/editing/deleting. This is an additional check done
    # after the permissions for the object has been checked - everyone needs to be able to edit the
    # same content on the same page, so just allow all inlines.

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class StackedInline(InlineBlockModelAdmin):
    template = 'admin/edit_inline/stacked.html'


class TabularInline(InlineBlockModelAdmin):
    template = 'admin/edit_inline/tabular.html'


site = BlockAdminSite(name='block_admin')
