# Generated by Django 3.1.5 on 2021-07-23 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cragweather', '0007_auto_20210723_0211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cragmodel',
            name='crag_type',
        ),
    ]
