# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Version(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    version_number = models.PositiveIntegerField(db_index=True, null=True)
    template_name = models.CharField(max_length=70)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)

    class Meta:
        ordering = ('-version_number',)
        unique_together = (
            ('content_type', 'object_id', 'version_number'),
        )

    def __str__(self):
        if self.version_number:
            return 'Version %d' % (self.version_number,)
        else:
            return 'Unpublished version %s' % (self.created,)

    def generate_version(self):
        # Create a version number if the page doesn't have one already
        if not self.version_number:
            try:
                prev_version = Version.objects.filter(
                    content_type=self.content_type, object_id=self.object_id).exclude(
                    version_number__isnull=True)[0].version_number
            except IndexError:
                prev_version = 0

            self.version_number = prev_version + 1

        return self.version_number

    @property
    def is_published(self):
        obj = self.content_object

        if self.version_number and obj.published and obj.current_version == self:
            return True
        else:
            return False


@python_2_unicode_compatible
class ContentBlock(models.Model):
    obj_version = models.ForeignKey(Version)
    column = models.CharField(max_length=100, db_index=True)
    position = models.IntegerField(null=True, db_index=True)
    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('position',)
        unique_together = (
            ('obj_version', 'column', 'position'),
        )

    def __str__(self):
        return self.content_type.name

    def save(self, *args, **kwargs):
        # Set the position to the highest possible if there isn't one already
        if self.position is None:
            last_position = ContentBlock.objects.filter(
                obj_version=self.obj_version, column=self.column).aggregate(
                models.Max('position'))['position__max']

            # Just incase it's the first block in this column
            if last_position is None:
                self.position = 1
            else:
                self.position = last_position + 1

        super(ContentBlock, self).save(*args, **kwargs)


class BaseBlock(models.Model):
    content_block = models.ForeignKey(ContentBlock, null=True, editable=False)

    # Override if more complex view logic is needed
    render_function = 'glitter.block_views.baseblock'

    class Meta:
        abstract = True
