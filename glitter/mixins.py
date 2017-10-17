# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import models

from glitter.exceptions import GlitterUnpublishedException
from glitter.models import Version
from glitter.page import Glitter

from .managers import GlitterManager


class GlitterMixin(models.Model):
    published = models.BooleanField(default=True, db_index=True)
    current_version = models.ForeignKey('glitter.Version', blank=True, null=True, editable=False)

    objects = GlitterManager()

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'edit', 'publish')
        abstract = True

    def get_latest_version(self):
        """ Get the latest version for the page. """
        content_type = ContentType.objects.get_for_model(self)
        latest_version = Version.objects.filter(
            content_type=content_type, object_id=self.id
        ).exclude(version_number=None).first()
        return latest_version

    @property
    def is_published(self):
        """
        Return a boolean if the object is fully published and visible.

        Glitter objects need to be published and have a current version to be visible to end users.
        """
        return self.published and self.current_version_id is not None


class GlitterDetailMixin(object):
    def post(self, request, *args, **kwargs):
        # By default detail views don't allow POST requests, however forms are usable as blocks.
        # So we allow POST requests, which does the same as GET.
        return self.get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(GlitterDetailMixin, self).get_object(queryset)

        version = self.kwargs.get('version')

        if version:
            self.glitter = Glitter(page_version=version, request=self.request)
        else:

            # If an object isn't viewable by end users - staff might still be able to edit the
            # object. Raise an exception and let middleware deal with it.
            if not obj.published or not obj.current_version:
                raise GlitterUnpublishedException(obj=obj)
            self.glitter = Glitter(page_version=obj.current_version, request=self.request)

        self.glitter_columns = self.glitter.render()

        return obj

    def get_template_names(self):
        return [self.glitter.version.template_name]

    def get_context_data(self, **kwargs):
        context = super(GlitterDetailMixin, self).get_context_data(**kwargs)

        obj = self.get_object()
        edit = self.kwargs.get('edit_mode')

        columns = self.glitter.render(edit_mode=edit)

        context['glitter'] = self.glitter
        context['columns'] = columns
        context['edit_mode'] = edit
        context[obj._meta.model_name] = obj
        return context
