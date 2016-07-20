# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import title
from django.templatetags.i18n import language_name_local
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
    url = models.CharField('URL', max_length=100, validators=[validate_page_url])
    title = models.CharField(max_length=100)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    login_required = models.BooleanField(default=False)
    show_in_navigation = models.BooleanField(default=True, db_index=True)
    unpublished_count = models.PositiveIntegerField(default=0, editable=False)
    language = models.CharField(max_length=10, blank=True)

    objects = PageManager()

    def __str__(self):
        string = '%s -- %s' % (self.title, self.url)
        if self.is_languages_required():
            string = '{} -- {} -- {}'.format(self.title, self.language, self.url)
        return string

    class Meta(GlitterMixin.Meta):
        verbose_name = 'page'
        ordering = ('url',)
        unique_together = ('url', 'language')
        permissions = (
            ('view_protected_page', 'Can view protected page'),
        )

    def get_page_languages(self):
        """ Get all languages for given page. """
        return self._meta.model.objects.filter(url=self.url)

    def get_languages_link(self):
        """ Get languages link for pages. """
        data = {}
        pages = {x.language: x.url for x in self.get_page_languages()}
        for key, val in dict(settings.PAGE_LANGUAGES).items():
            language_name = title(language_name_local(key))
            if pages.get(key):
                data[language_name] = '/{}{}'.format(key, pages.get(key))
            else:
                data[language_name] = '/{}/'.format(key)
        return data

    @staticmethod
    def is_languages_required():
        if hasattr(settings, 'PAGE_LANGUAGES'):
            return True
        return False

    @staticmethod
    def is_login_required():
        if hasattr(settings, 'GLITTER_SHOW_LOGIN_REQUIRED'):
            return getattr(settings, 'GLITTER_SHOW_LOGIN_REQUIRED')
        return False

    def get_absolute_url(self):
        url = self.url
        if hasattr(settings, 'PAGE_LANGUAGES'):
            url = '/{}{}'.format(self.language, self.url)
        return url

    def save(self, *args, **kwargs):
        # Find the number of unpublished pages
        content_type = ContentType.objects.get_for_model(self)
        unpublished_pages = Version.objects.filter(
            content_type=content_type, object_id=self.id
        ).exclude(version_number__isnull=True)

        if self.current_version:
            unpublished_pages = unpublished_pages.filter(
                version_number__gt=self.current_version.version_number
            )

        self.unpublished_count = unpublished_pages.count()
        super(Page, self).save(*args, **kwargs)
