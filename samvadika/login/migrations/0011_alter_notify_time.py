# Generated by Django 3.2.8 on 2021-10-24 21:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_notify_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notify',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]