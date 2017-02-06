# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import glitter.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_banner', '0002_linkfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='link',
            field=glitter.fields.LinkField(blank=True, max_length=254),
        ),
    ]
