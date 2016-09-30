# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import glitter.pages.validators


class Migration(migrations.Migration):

    dependencies = [
        ('glitter_pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='language',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='url',
            field=models.CharField(max_length=100, verbose_name='URL', validators=[glitter.pages.validators.validate_page_url]),
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('url', 'language')]),
        ),
    ]
