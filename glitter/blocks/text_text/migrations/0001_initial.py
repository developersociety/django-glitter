# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextTextBlock',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('block_class', models.CharField(verbose_name='Class', max_length=50)),
                ('left_column', models.TextField()),
                ('right_column', models.TextField()),
                ('content_block', models.ForeignKey(editable=False, null=True, to='glitter.ContentBlock')),
            ],
            options={
                'verbose_name': 'two column text',
            },
        ),
    ]
