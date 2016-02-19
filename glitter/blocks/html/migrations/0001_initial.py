# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HTML',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('content', models.TextField()),
                ('content_block', models.ForeignKey(null=True, editable=False, to='glitter.ContentBlock')),
            ],
            options={
                'verbose_name': 'HTML',
            },
        ),
    ]
