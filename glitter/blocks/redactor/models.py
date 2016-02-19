# -*- coding: utf-8 -*-

from django.db import models

from glitter.models import BaseBlock


class BaseRedactorBlock(BaseBlock):
    block_class = models.CharField('Class', max_length=50)
    content = models.TextField()

    class Meta:
        abstract = True


class Redactor(BaseRedactorBlock):
    class Meta:
        verbose_name = 'text'
