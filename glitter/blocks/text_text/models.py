# -*- coding: utf-8 -*-

from django.db import models

from glitter.models import BaseBlock


class BaseTextTextBlock(BaseBlock):
    block_class = models.CharField('Class', max_length=50)
    left_column = models.TextField()
    right_column = models.TextField()

    class Meta:
        abstract = True


class TextTextBlock(BaseTextTextBlock):
    class Meta:
        verbose_name = 'two column text'
