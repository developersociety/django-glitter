# -*- coding: utf-8 -*-

from glitter.models import BaseBlock

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class SampleModel(models.Model):
    content = models.TextField(blank=True)

    def __str__(self):
        return self.content


class SampleModelWithInlinesBlock(BaseBlock):
    pass


@python_2_unicode_compatible
class SampleInline(models.Model):
    parent_block = models.ForeignKey(SampleModelWithInlinesBlock)
    foreign_model = models.ForeignKey(SampleModel, on_delete=models.PROTECT)

    def __str__(self):
        return '%s' % (self.foreign_model,)
