# Generated by Django 5.0 on 2023-12-20 17:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("habits", "0012_category_color_habit_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="habit",
            name="status",
        ),
    ]
