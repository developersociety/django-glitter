# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0003_auto_20170317_1254'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reminder',
            old_name='date_sent',
            new_name='sent_at',
        ),
    ]
