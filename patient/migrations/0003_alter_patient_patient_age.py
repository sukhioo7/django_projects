# Generated by Django 5.0 on 2024-01-12 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("patient", "0002_rename_patietn_city_patient_patient_city_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="patient_age",
            field=models.PositiveSmallIntegerField(),
        ),
    ]
