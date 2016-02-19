# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Redactor',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('block_class', models.CharField(verbose_name='Class', max_length=50)),
                ('content', models.TextField()),
                ('content_block', models.ForeignKey(null=True, to='glitter.ContentBlock', editable=False)),
            ],
            options={
                'verbose_name': 'text',
            },
        ),
    ]
