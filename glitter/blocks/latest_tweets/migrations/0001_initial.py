# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LatestTweetsBlock',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('user', models.CharField(blank=True, max_length=15)),
                ('content_block', models.ForeignKey(null=True, to='glitter.ContentBlock', editable=False)),
            ],
            options={
                'verbose_name': 'latest tweets',
            },
        ),
    ]
