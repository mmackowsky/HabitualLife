# Generated by Django 5.0 on 2024-01-04 15:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("habits", "0022_habit_interval_value_alter_habit_frequency"),
    ]

    operations = [
        migrations.AddField(
            model_name="habit",
            name="streak_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="habit",
            name="frequency",
            field=models.CharField(
                choices=[("DAILY", "Daily"), ("INTERVAL", "Interval")],
                default=None,
                max_length=10,
            ),
        ),
    ]
