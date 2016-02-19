# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallToActionBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('link', models.URLField()),
                ('content_block', models.ForeignKey(null=True, to='glitter.ContentBlock', editable=False)),
            ],
            options={
                'verbose_name': 'call to action',
            },
        ),
    ]
