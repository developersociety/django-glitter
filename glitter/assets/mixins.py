# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class FileMixin(models.Model):
    class Meta:
        abstract = True
        ordering = ('-created_at', '-modified_at', 'title')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.file.url

    def save(self, *args, **kwargs):
        # Avoid doing file size requests constantly
        self.file_size = self.file.size

        super(FileMixin, self).save(*args, **kwargs)
