# Generated by Django 3.2.15 on 2022-12-11 13:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20221211_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 11, 14, 33, 5, 792297)),
        ),
    ]
