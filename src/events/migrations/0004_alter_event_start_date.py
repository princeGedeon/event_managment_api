# Generated by Django 4.1.5 on 2023-01-11 15:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_event_status_alter_event_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 11, 16, 0, 32, 943085), verbose_name="Date de debut de l'évenement"),
        ),
    ]
