# Generated by Django 5.0 on 2023-12-29 10:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("habits", "0017_alter_habit_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habit",
            name="active",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="habit",
            name="frequency",
            field=models.CharField(
                choices=[
                    ("DAILY", "Daily"),
                    ("INTERVAL", "Interval"),
                    ("MONTHLY", "Monthly"),
                ],
                default=None,
                max_length=10,
            ),
        ),
    ]
