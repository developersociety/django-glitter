# -*- coding: utf-8 -*-

from django.db import models


class GlitterManager(models.Manager):
    def published(self):
        return self.filter(published=True).exclude(current_version=None)

    def unpublished(self):
        return self.filter(published=True, current_version__isnull=True)
