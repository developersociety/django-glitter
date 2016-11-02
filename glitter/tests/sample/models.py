# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from glitter.mixins import GlitterMixin


@python_2_unicode_compatible
class Book(GlitterMixin):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
