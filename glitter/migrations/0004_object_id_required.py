# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0003_remove_empty_contentblocks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentblock',
            name='object_id',
            field=models.PositiveIntegerField(),
        ),
    ]
