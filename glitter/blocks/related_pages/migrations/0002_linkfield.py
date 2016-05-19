# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import glitter.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_related_pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relatedpage',
            name='link',
            field=glitter.fields.LinkField(default='', max_length=254, blank=True),
            preserve_default=False,
        ),
    ]
