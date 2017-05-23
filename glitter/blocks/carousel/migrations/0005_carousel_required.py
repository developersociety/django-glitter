# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_carousel', '0004_delete_empty_blocks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carouselblock',
            name='carousel',
            field=models.ForeignKey(to='glitter_carousel.Carousel', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='imageonlycarouselblock',
            name='carousel',
            field=models.ForeignKey(to='glitter_carousel.ImageOnlyCarousel', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
