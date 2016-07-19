# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='language',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
