# Generated by Django 3.1.7 on 2021-10-16 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_savequestion'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='savequestion',
            unique_together={('threadid', 'user_name')},
        ),
    ]
