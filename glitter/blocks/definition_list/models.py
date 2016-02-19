# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from glitter.models import BaseBlock


class DefinitionList(BaseBlock):
    class Meta:
        verbose_name = 'Definition list'


@python_2_unicode_compatible
class DefinitionListInline(models.Model):
    definition_list = models.ForeignKey(DefinitionList)
    key = models.CharField(max_length=128)
    value = models.TextField()

    def __str__(self):
        return ''
