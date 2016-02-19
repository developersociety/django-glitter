# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import glitter.blocks.video.validators


class Migration(migrations.Migration):

    dependencies = [
        ('glitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('url', models.URLField(validators=[glitter.blocks.video.validators.validate_url], help_text='YouTube, Vimeo videos only', verbose_name='URL')),
                ('html', models.TextField(editable=False)),
                ('content_block', models.ForeignKey(editable=False, to='glitter.ContentBlock', null=True)),
            ],
            options={
                'verbose_name': 'video',
            },
        ),
    ]
