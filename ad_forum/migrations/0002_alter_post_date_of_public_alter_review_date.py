# Generated by Django 4.0.4 on 2022-05-10 17:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad_forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_of_public',
            field=models.DateField(default=datetime.date(2022, 5, 10)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(default=datetime.date(2022, 5, 10)),
        ),
    ]
