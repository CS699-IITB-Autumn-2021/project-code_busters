# Generated by Django 3.2.8 on 2021-10-24 21:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_rename_notify_notify_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='notify',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 24, 21, 6, 59, 729121, tzinfo=utc)),
        ),
    ]