# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_banner', '0004_delete_empty_blocks'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bannerinline',
            options={'ordering': ('position', 'id'), 'verbose_name': 'banner'},
        ),
        migrations.AddField(
            model_name='bannerinline',
            name='position',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]
