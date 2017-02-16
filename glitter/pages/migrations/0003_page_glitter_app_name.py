# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_pages', '0002_page_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='glitter_app_name',
            field=models.CharField(verbose_name='Glitter App', db_index=True, max_length=255, blank=True),
        ),
    ]
