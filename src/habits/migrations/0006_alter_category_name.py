# Generated by Django 4.2.7 on 2023-12-14 11:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("habits", "0005_alter_habit_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]
