# Generated by Django 5.0 on 2024-01-09 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("patient", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="patient",
            old_name="patietn_city",
            new_name="patient_city",
        ),
        migrations.AlterField(
            model_name="patient",
            name="patient_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
