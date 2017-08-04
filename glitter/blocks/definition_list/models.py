from django.db import models

from glitter.models import BaseBlock


class DefinitionList(BaseBlock):
    class Meta:
        verbose_name = 'Definition list'


class DefinitionListInline(models.Model):
    definition_list = models.ForeignKey(DefinitionList)
    key = models.CharField(max_length=128)
    value = models.TextField()

    def __str__(self):
        return ''
