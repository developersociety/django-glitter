# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import glitter.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_image', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageblock',
            name='link',
            field=glitter.fields.LinkField(blank=True, max_length=254),
        ),
    ]
