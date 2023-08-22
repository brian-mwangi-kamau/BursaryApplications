# Generated by Django 4.1.3 on 2023-08-22 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Application", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Application",
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
                ("student_name", models.CharField(max_length=255)),
                ("school_name", models.CharField(max_length=255)),
                ("admission_number", models.CharField(max_length=20)),
                ("year_of_study", models.CharField(max_length=50)),
                ("constituency", models.CharField(max_length=15)),
                ("location", models.CharField(max_length=15)),
                ("phone_number", models.CharField(max_length=10)),
                ("id_number", models.CharField(max_length=8)),
                ("submission_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
