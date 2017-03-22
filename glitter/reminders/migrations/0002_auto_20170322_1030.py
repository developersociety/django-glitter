# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='sent_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='reminder',
            unique_together=set([('user', 'object_id', 'content_type')]),
        ),
    ]
