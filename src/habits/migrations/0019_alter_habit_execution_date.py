# Generated by Django 5.0 on 2023-12-29 12:41

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("habits", "0018_alter_habit_active_alter_habit_frequency"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habit",
            name="execution_date",
            field=models.DateField(default=datetime.date(2023, 12, 29)),
        ),
    ]
