# -*- coding: utf-8 -*-

from functools import update_wrapper

from django.apps import apps
from django.contrib import admin
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.admin.options import csrf_protect_m
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, resolve
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.views.decorators.http import require_POST

from .forms import get_addblock_form, get_movecolumn_form, get_newpagetemplateform, MoveBlockForm
from .models import ContentBlock, Version
from .page import Glitter
from .signals import page_version_published, page_version_saved, page_version_unpublished
from .templates import get_layout
from .utils import duplicate, JSONEncoderForHTML
from .views import render_page


require_post_m = method_decorator(require_POST)


class GlitterPagePublishedFilter(admin.SimpleListFilter):
    title = 'published'
    parameter_name = 'published'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Yes'),
            ('0', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(published=True).exclude(current_version=None)

        if self.value() == '0':
            return queryset.filter(published=True, current_version__isnull=True)


class GlitterAdminMixin(object):
    list_filter = (GlitterPagePublishedFilter,)
    glitter_render = None

    def is_published(self, obj):
        return obj.published and obj.current_version_id is not None
    is_published.boolean = True
    is_published.short_description = 'Published'

    def get_urls(self):
        from django.conf.urls import url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            # Start a page with a brand new template
            url(r'^(?P<object_id>\d+)/template/$',
                wrap(self.page_template_view),
                name='%s_%s_template' % info),

            # Redirect a user to view the latest appropriate page
            url(r'^(?P<object_id>\d+)/redirect/$',
                wrap(self.page_redirect_view),
                name='%s_%s_redirect' % info),

            # View and edit
            url(r'^editor/view/(?P<version_id>\d+)/$',
                wrap(self.page_version_view),
                name='%s_%s_version' % info),
            url(r'^editor/edit/(?P<version_id>\d+)/$',
                wrap(self.page_edit_view),
                name='%s_%s_edit' % info),

            # Change template
            url(r'^editor/changetemplate/(?P<version_id>\d+)/$',
                wrap(self.page_changetemplate_view),
                name='%s_%s_changetemplate' % info),

            # Save, publish, discard
            url(r'^edit/page/(?P<version_id>\d+)/save/$',
                wrap(self.page_save_view),
                name='%s_%s_save' % info),
            url(r'^edit/page/(?P<version_id>\d+)/publish/$',
                wrap(self.page_publish_view),
                name='%s_%s_publish' % info),
            url(r'^edit/page/(?P<version_id>\d+)/unpublish/$',
                wrap(self.page_unpublish_view),
                name='%s_%s_unpublish' % info),
            url(r'^edit/page/(?P<version_id>\d+)/discard/$',
                wrap(self.page_discard_view),
                name='%s_%s_discard' % info),

            # Block add
            url(r'^edit/page/(?P<version_id>\d+)/block/add/$',
                wrap(self.page_block_add_view),
                name='%s_%s_block_add' % info),

            # Block editing/updating/moving
            url(r'^edit/block/del/(?P<contentblock_id>\d+)/$',
                wrap(self.page_block_delete_view),
                name='%s_%s_block_delete' % info),
            url(r'^edit/block/move/(?P<contentblock_id>\d+)/$',
                wrap(self.page_block_move_view),
                name='%s_%s_block_move' % info),
            url(r'^edit/block/column/(?P<contentblock_id>\d+)/$',
                wrap(self.page_block_column_view),
                name='%s_%s_block_column' % info),

        ] + super(GlitterAdminMixin, self).get_urls()
        return urlpatterns

    def has_edit_permission(self, request, obj=None, version=None):
        """
        Returns a boolean if the user in the request has edit permission for the object.

        Can also be passed a version object to check if the user has permission to edit a version
        of the object (if they own it).
        """
        # Has the edit permission for this object type
        permission_name = '{}.edit_{}'.format(self.opts.app_label, self.opts.model_name)
        has_permission = request.user.has_perm(permission_name)

        if obj is not None and has_permission is False:
            has_permission = request.user.has_perm(permission_name, obj=obj)

        if has_permission and version is not None:
            # Version must not be saved, and must belong to this user
            if version.version_number or version.owner != request.user:
                has_permission = False

        return has_permission

    def has_publish_permission(self, request, obj=None):
        """
        Returns a boolean if the user in the request has publish permission for the object.
        """
        permission_name = '{}.publish_{}'.format(self.opts.app_label, self.opts.model_name)
        has_permission = request.user.has_perm(permission_name)

        if obj is not None and has_permission is False:
            has_permission = request.user.has_perm(permission_name, obj=obj)

        return has_permission

    def response_add(self, request, obj, *args, **kwargs):
        if '_saveandedit' in request.POST:
            return self.page_redirect(request, obj)
        else:
            return super(GlitterAdminMixin, self).response_add(request, obj, *args, **kwargs)

    def response_change(self, request, obj, *args, **kwargs):
        if '_saveandedit' in request.POST:
            return self.page_redirect(request, obj)
        else:
            return super(GlitterAdminMixin, self).response_change(request, obj, *args, **kwargs)

    @csrf_protect_m
    @transaction.atomic
    def page_template_view(self, request, object_id):
        obj = get_object_or_404(self.model, id=object_id)

        if not self.has_edit_permission(request, obj):
            raise PermissionDenied

        NewPageTemplateForm = get_newpagetemplateform(model=self.model)
        form = NewPageTemplateForm(request.POST or None)

        if form.is_valid():
            version = form.save(commit=False)
            version.content_type = self.content_type
            version.object_id = obj.id
            version.owner = request.user
            version.save()

            opts = self.opts.app_label, self.opts.model_name
            return HttpResponseRedirect(reverse('admin:%s_%s_version' % opts, kwargs={
                'version_id': version.id,
            }))

        return TemplateResponse(request, 'admin/glitter/new_template.html', {
            'form': form,
        })

    def page_redirect(self, request, obj):
        opts = self.opts.app_label, self.opts.model_name

        if not self.has_edit_permission(request, obj):
            raise PermissionDenied

        # Redirect a user to the published page if it has one
        if obj.current_version:
            return HttpResponseRedirect(obj.get_absolute_url())

        # Otherwise we'll go for the latest version a user has access to
        try:
            version = Version.objects.filter(
                content_type=ContentType.objects.get_for_model(obj), object_id=obj.id).exclude(
                ~Q(owner=request.user), version_number__isnull=True)[0]
            return HttpResponseRedirect(reverse('admin:%s_%s_version' % opts, kwargs={
                'version_id': version.id,
            }))
        except IndexError:
            pass

        # Last resort is getting the user to create a new page with a new template
        return HttpResponseRedirect(reverse('admin:%s_%s_template' % opts, kwargs={
            'object_id': obj.id,
        }))

    def page_redirect_view(self, request, object_id):
        page = get_object_or_404(self.model, id=object_id)
        return self.page_redirect(request, page)

    def page_version_view(self, request, version_id):
        version = get_object_or_404(self.version_queryset().select_related(), id=version_id)

        obj = version.content_object

        if not self.has_edit_permission(request, obj):
            raise PermissionDenied

        # Deny other users from viewing an unsaved version
        if not version.version_number and version.owner != request.user:
            raise PermissionDenied

        if not self.glitter_render:
            func, args, kwargs = resolve(obj.get_absolute_url())
            kwargs['edit_mode'] = False
            kwargs['version'] = version
            response = func(request, *args, **kwargs)
            return response
        else:
            return render_page(request, obj, version)

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self.model)

    def version_queryset(self):
        return Version.objects.filter(content_type=self.content_type)

    def contentblock_queryset(self):
        return ContentBlock.objects.filter(obj_version__content_type=self.content_type)

    @csrf_protect_m
    @transaction.atomic
    def page_edit_view(self, request, version_id):
        opts = self.opts.app_label, self.opts.model_name

        version = get_object_or_404(self.version_queryset().select_related(), id=version_id)

        obj = version.content_object

        if not self.has_edit_permission(request, obj):
            raise PermissionDenied

        # Deny other users from viewing an unsaved version
        if not version.version_number and version.owner != request.user:
            raise PermissionDenied

        # POST request to initiate
        if request.method == 'POST':
            # No need to copy a version if they're still editing it
            if not version.version_number:
                return HttpResponseRedirect(reverse('admin:%s_%s_edit' % opts, kwargs={
                    'version_id': version_id,
                }))

            # Create a copy of this version for the user
            new_version = Version.objects.create(
                content_type=self.content_type,
                object_id=obj.id,
                template_name=version.template_name,
                owner=request.user)

            for content_block in version.contentblock_set.all():
                # Copy the block
                new_block = duplicate(content_block.content_object)
                new_block.save()

                # Copy the content block
                new_content_block = content_block
                new_content_block.id = None
                new_content_block.content_object = new_block
                new_content_block.obj_version = new_version
                new_content_block.save()

                # Point the block back to the ContentBlock
                new_block.content_block = new_content_block
                new_block.save()

            return HttpResponseRedirect(reverse('admin:%s_%s_edit' % opts, kwargs={
                'version_id': new_version.id,
            }))

        # Redirect to view if the version is already saved
        if version.version_number:
            return HttpResponseRedirect(reverse('admin:%s_%s_version' % opts, kwargs={
                'version_id': version_id,
            }))

        if not self.glitter_render:
            request = request
            func, args, kwargs = resolve(obj.get_absolute_url())
            kwargs['edit_mode'] = True
            kwargs['version'] = version
            response = func(request, *args, **kwargs)
            return response
        else:
            return render_page(request, obj, version, edit=True)

    @csrf_protect_m
    @transaction.atomic
    def page_changetemplate_view(self, request, version_id):
        version = get_object_or_404(self.version_queryset().select_related(), id=version_id)
        obj = version.content_object

        if not self.has_edit_permission(request, obj):
            raise PermissionDenied

        # Can't change a saved version
        if version.version_number:
            raise PermissionDenied

        old_template = get_layout(template_name=version.template_name)
        NewPageTemplateForm = get_newpagetemplateform(model=self.model)
        form = NewPageTemplateForm(request.POST, instance=version)

        # Deny other users from viewing an unsaved version
        if not version.version_number and version.owner != request.user:
            raise PermissionDenied

        if form.is_valid():
            version = form.save()
            new_template = get_layout(template_name=version.template_name)

            # If any columns don't exist in the new template, default them to the first column
            for i in old_template._meta.columns:
                if i not in new_template._meta.columns:
                    # Find the first column to put this content in - sadly this is currently the
                    # first column alphabetically for consistency. In future this will be the first
                    # column defined (the most important one).
                    new_column = sorted(new_template._meta.columns.keys())[0]

                    # Find the last block in the new first column
                    last_block = ContentBlock.objects.filter(
                        obj_version=version, column=new_column).last()

                    if last_block is not None:
                        next_position = last_block.position + 1
                    else:
                        next_position = 1

                    # Append to the first column
                    for content in ContentBlock.objects.filter(obj_version=version, column=i):
                        content.column = new_column
                        content.position = next_position
                        content.save()
                        next_position += 1

        opts = self.opts.app_label, self.opts.model_name
        return HttpResponseRedirect(reverse('admin:%s_%s_edit' % opts, kwargs={
            'version_id': version_id,
        }))

    @csrf_protect_m
    @require_post_m
    @transaction.atomic
    def page_save_view(self, request, version_id):
        version = get_object_or_404(self.version_queryset().select_related(), id=version_id)
        obj = version.content_object

        if not self.has_edit_permission(request, obj):
            raise PermissionDenied

        # Deny other users from saving a users version
        if version.owner != request.user:
            raise PermissionDenied

        # No need for errors, save anything and only update unsaved versions
        if not version.version_number:
            version.generate_version()
            version.save()

            page_version_saved.send(
                sender=obj.__class__,
                obj=obj,
                version=version,
                user=request.user)

        opts = self.opts.app_label, self.opts.model_name
        return HttpResponseRedirect(reverse('admin:%s_%s_version' % opts, kwargs={
            'version_id': version_id,
        }))

    @csrf_protect_m
    @require_post_m
    @transaction.atomic
    def page_publish_view(self, request, version_id):
        version = get_object_or_404(self.version_queryset().select_related(), id=version_id)
        obj = version.content_object

        if not self.has_publish_permission(request, obj):
            raise PermissionDenied

        # Deny other users from publishing an unsaved version
        if not version.version_number and version.owner != request.user:
            raise PermissionDenied

        # Repeated publish - ignore
        if obj.current_version == version:
            return HttpResponseRedirect(obj.get_absolute_url())

        # Save the page if it isn't already
        if not version.version_number:
            version.generate_version()
            version.save()

            page_version_saved.send(
                sender=obj.__class__,
                obj=obj,
                version=version,
                publish=True,
                user=request.user)

        # Publish!
        previous_version = obj.current_version
        obj.current_version = version
        obj.save()

        page_version_published.send(
            sender=obj.__class__,
            obj=obj,
            version=version,
            previous_version=previous_version,
            user=request.user)

        message = 'Published version %d' % (version.version_number,)
        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=self.content_type.pk,
            object_id=obj.id,
            object_repr=force_text(obj),
            action_flag=CHANGE,
            change_message=message
        )

        return HttpResponseRedirect(obj.get_absolute_url())

    @csrf_protect_m
    @require_post_m
    @transaction.atomic
    def page_unpublish_view(self, request, version_id):
        version = get_object_or_404(self.version_queryset().select_related(), id=version_id)
        obj = version.content_object

        if not self.has_publish_permission(request, obj):
            raise PermissionDenied

        # Not the current version? Just ignore the action and view the page again
        if obj.current_version == version:
            obj.current_version = None
            message = 'Unpublished page'

            page_version_unpublished.send(
                sender=obj.__class__,
                obj=obj,
                version=version,
                user=request.user)
            obj.save()

            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=self.content_type.pk,
                object_id=obj.id,
                object_repr=force_text(obj),
                action_flag=CHANGE,
                change_message=message
            )

        opts = self.opts.app_label, self.opts.model_name
        return HttpResponseRedirect(reverse('admin:%s_%s_version' % opts, kwargs={
            'version_id': version.id,
        }))

    @csrf_protect_m
    @transaction.atomic
    def page_discard_view(self, request, version_id):
        version = get_object_or_404(self.version_queryset().select_related(), id=version_id)
        obj = version.content_object

        if not self.has_edit_permission(request, obj, version=version):
            raise PermissionDenied

        # POST request to initiate
        if request.method == 'POST':
            # Remove all blocks
            for i in version.contentblock_set.all():
                i.delete()

            version.delete()

            return TemplateResponse(request, 'admin/glitter/version_discarded.html', {
                'obj': obj,
                'opts': self.model._meta,
            }, current_app=self.admin_site.name)

        return TemplateResponse(
            request, 'admin/glitter/version_discard.html', current_app=self.admin_site.name)

    @csrf_protect_m
    @transaction.atomic
    def page_block_add_view(self, request, version_id):
        version = get_object_or_404(self.version_queryset().select_related(), id=version_id)
        obj = version.content_object

        if not self.has_edit_permission(request, obj, version=version):
            raise PermissionDenied

        AddBlockForm = get_addblock_form(version)
        form = AddBlockForm(request.POST, instance=ContentBlock(obj_version=version))

        response_dict = {}

        if form.is_valid():
            # Figure out the block type we need
            new_obj_class = form.cleaned_data['block_type']
            app_name, model_name = new_obj_class.split('.', 1)
            new_obj_class = apps.get_model(app_name, model_name)

            # Create the block
            block = new_obj_class.objects.create()

            # Create a ContentBlock pointing to it
            content_block = form.save(commit=False)
            content_block.content_object = block

            if form.cleaned_data['top']:
                # User wants block at the top of the column, so set the position or it'll end up
                # being autosaved to the end of the column
                first_block = ContentBlock.objects.filter(
                    obj_version=version, column=content_block.column).first()

                if first_block is not None:
                    content_block.position = first_block.position - 1

            content_block.save()

            # Point the block back to the ContentBlock
            block.content_block = content_block
            block.save()

            # Updated the modified timestamp
            version.save()

            # Render the updated column
            response_dict['column'] = slugify(content_block.column)
            glitter = Glitter(version, request=request)
            columns = glitter.render(edit_mode=True, rerender=True)
            response_dict['content'] = columns[content_block.column]

        return JsonResponse(response_dict)

    @csrf_protect_m
    @transaction.atomic
    def page_block_delete_view(self, request, contentblock_id):
        content_block = get_object_or_404(self.contentblock_queryset(), id=contentblock_id)
        block = content_block.content_object
        version = content_block.obj_version
        obj = version.content_object

        if not self.has_edit_permission(request, obj, version=version):
            raise PermissionDenied

        if request.POST:
            # Save variables for use after deletion
            column = content_block.column

            # Delete the block
            content_block.delete()
            block.delete()

            # Render the updated column as a JSON object
            glitter = Glitter(version, request=request)
            columns = glitter.render(edit_mode=True, rerender=True)
            rendered_json = JSONEncoderForHTML().encode({
                'content': columns[column],
            })

            return TemplateResponse(request, 'admin/glitter/update_column.html', {
                'column': slugify(column),
                'rendered_json': rendered_json,
            }, current_app=self.admin_site.name)

        return TemplateResponse(request, 'admin/glitter/block_delete.html', {
            'content_block': block,
        }, current_app=self.admin_site.name)

    @csrf_protect_m
    @transaction.atomic
    def page_block_move_view(self, request, contentblock_id):
        content_block = get_object_or_404(self.contentblock_queryset(), id=contentblock_id)
        version = content_block.obj_version
        obj = version.content_object

        if not self.has_edit_permission(request, obj, version=version):
            raise PermissionDenied

        form = MoveBlockForm(request.POST)
        response_dict = {}

        if form.is_valid():
            move = form.cleaned_data['move']

            if move == MoveBlockForm.MOVE_UP or move == MoveBlockForm.MOVE_DOWN:
                # Move up/down involve swapping block positions

                try:
                    if move == MoveBlockForm.MOVE_UP:
                        other_block = ContentBlock.objects.filter(
                            obj_version=version,
                            column=content_block.column,
                            position__lt=content_block.position).order_by('-position')[0]
                    else:
                        other_block = ContentBlock.objects.filter(
                            obj_version=version,
                            column=content_block.column,
                            position__gt=content_block.position)[0]

                    old_position = content_block.position
                    new_position = other_block.position

                    # Temporarily unset other_block's position
                    other_block.position = None
                    other_block.save()

                    # Now set the appropriate positions
                    content_block.position = new_position
                    content_block.save()

                    other_block.position = old_position
                    other_block.save()

                except IndexError:
                    # User tried to move a block too far
                    pass

            else:
                if move == MoveBlockForm.MOVE_TOP:
                    # Move to top requires setting the position to one less than the first
                    other_block = ContentBlock.objects.filter(
                        obj_version=version, column=content_block.column)[0]

                    # This could be the first block
                    if content_block != other_block:
                        content_block.position = other_block.position - 1
                        content_block.save()
                else:
                    # Move bottom requires setting the position to one greater than the last
                    other_block = ContentBlock.objects.filter(
                        obj_version=version,
                        column=content_block.column).order_by('-position')[0]

                    # This could be the last block
                    if content_block != other_block:
                        content_block.position = other_block.position + 1
                        content_block.save()

            response_dict['column'] = slugify(content_block.column)
            glitter = Glitter(version, request=request)
            columns = glitter.render(edit_mode=True, rerender=True)
            response_dict['content'] = columns[content_block.column]

        return JsonResponse(response_dict)

    @csrf_protect_m
    @transaction.atomic
    def page_block_column_view(self, request, contentblock_id):
        content_block = get_object_or_404(self.contentblock_queryset(), id=contentblock_id)
        version = content_block.obj_version
        obj = version.content_object

        if not self.has_edit_permission(request, obj, version=version):
            raise PermissionDenied

        # Need to build a form which only has viable column moves
        template_obj = get_layout(template_name=version.template_name)
        column_choices = list(template_obj._meta.columns)
        column_choices.remove(content_block.column)

        MoveColumnForm = get_movecolumn_form(column_choices)
        form = MoveColumnForm(request.POST)
        response_dict = {}

        if form.is_valid():
            move = form.cleaned_data['move']
            source_column = content_block.column

            content_block.column = move

            # Find the last block of the column we're moving to
            if ContentBlock.objects.filter(
                    obj_version=version, column=move
            ).order_by('-position').exists():
                last_block = ContentBlock.objects.filter(
                    obj_version=version, column=move
                ).order_by('-position')[0]
                content_block.position = last_block.position + 1

            content_block.save()

            # Setup the page that can render both updated columns
            glitter = Glitter(version, request=request)
            columns = glitter.render(edit_mode=True, rerender=True)

            # Old column needs rendering again
            response_dict['source_column'] = slugify(source_column)
            response_dict['source_content'] = columns[source_column]

            # Now render the destination column
            response_dict['dest_column'] = slugify(content_block.column)
            response_dict['dest_content'] = columns[content_block.column]

        return JsonResponse(response_dict)
