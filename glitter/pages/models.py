# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey

from glitter.mixins import GlitterMixin
from glitter.models import Version
from .validators import validate_page_url


class PageManager(TreeManager):
    def published(self):
        return self.filter(published=True).exclude(current_version=None)

    def unpublished(self):
        return self.filter(published=True, current_version__isnull=True)


@python_2_unicode_compatible
class Page(MPTTModel, GlitterMixin):
    url = models.CharField('URL', max_length=100, unique=True, validators=[validate_page_url])
    title = models.CharField(max_length=100)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    login_required = models.BooleanField(default=False)
    show_in_navigation = models.BooleanField(default=True, db_index=True)
    unpublished_count = models.PositiveIntegerField(default=0, editable=False)

    objects = PageManager()

    def __str__(self):
        return '%s -- %s' % (self.title, self.url)

    class Meta(GlitterMixin.Meta):
        verbose_name = 'page'
        ordering = ('url',)
        permissions = (
            ('view_protected_page', 'Can view protected page'),
        )

    def get_absolute_url(self):
        return self.url

    def save(self, *args, **kwargs):
        # Find the number of unpublished pages
        unpublished_pages = Version.objects.filter(
            content_type=ContentType.objects.get_for_model(self), object_id=self.id).exclude(
            version_number__isnull=True)

        if self.current_version:
            unpublished_pages = unpublished_pages.filter(
                version_number__gt=self.current_version.version_number)

        self.unpublished_count = unpublished_pages.count()

        super(Page, self).save(*args, **kwargs)
