# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_carousel', '0002_linkfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carouselimage',
            name='subtitle',
            field=models.TextField(blank=True),
        ),
    ]
