# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0002_reminder_date_set'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reminder',
            old_name='date_set',
            new_name='date_sent',
        ),
    ]
