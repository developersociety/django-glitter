# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_related_pages', '0002_linkfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='relatedpage',
            name='new_window',
            field=models.BooleanField(verbose_name='Open link in new window', default=False),
        ),
    ]
