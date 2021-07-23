# Generated by Django 3.1.5 on 2021-07-23 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cragweather', '0006_auto_20210722_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationmodel',
            name='id',
        ),
        migrations.RemoveField(
            model_name='locationmodel',
            name='number_crags',
        ),
        migrations.AddField(
            model_name='locationmodel',
            name='location_key',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]