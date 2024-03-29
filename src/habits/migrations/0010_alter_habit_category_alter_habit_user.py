# Generated by Django 4.2.7 on 2023-12-14 14:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
        ("habits", "0009_alter_habit_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habit",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="habits",
                to="habits.category",
            ),
        ),
        migrations.AlterField(
            model_name="habit",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="habits",
                to="users.profile",
            ),
        ),
    ]
