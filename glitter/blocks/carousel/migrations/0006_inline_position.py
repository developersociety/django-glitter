# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_carousel', '0005_carousel_required'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carouselimage',
            options={'ordering': ('position', 'id')},
        ),
        migrations.AlterModelOptions(
            name='imageonlycarouselimage',
            options={'ordering': ('position', 'id')},
        ),
        migrations.AddField(
            model_name='carouselimage',
            name='position',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='imageonlycarouselimage',
            name='position',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]
