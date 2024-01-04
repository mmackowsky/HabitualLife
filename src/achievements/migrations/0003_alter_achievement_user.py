# Generated by Django 5.0 on 2024-01-04 16:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("achievements", "0002_remove_achievement_image"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="achievement",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.profile",
            ),
        ),
    ]
