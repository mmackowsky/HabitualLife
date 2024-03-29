# Generated by Django 4.2.7 on 2023-12-14 11:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("habits", "0003_category_unique_user_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                choices=[
                    ("HEALTH", "Health"),
                    ("FINANCE", "Finance"),
                    ("WORK", "Work"),
                ],
                max_length=100,
            ),
        ),
    ]
