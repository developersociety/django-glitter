# -*- coding: utf-8 -*-

from django.db import models

from glitter.models import BaseBlock


class LatestTweetsBlock(BaseBlock):
    user = models.CharField(max_length=15, blank=True)

    class Meta:
        verbose_name = 'latest tweets'
