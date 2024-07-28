# Generated by Django 5.0.7 on 2024-07-28 14:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("nationality", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Mobile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("model", models.CharField(max_length=100, unique=True)),
                ("price", models.PositiveIntegerField()),
                ("color", models.CharField(max_length=50)),
                ("screen_size", models.PositiveIntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[("+", "موجود"), ("-", "ناموجود")], max_length=1
                    ),
                ),
                ("manufacturer_country", models.CharField(max_length=100)),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.brand",
                    ),
                ),
            ],
        ),
    ]
