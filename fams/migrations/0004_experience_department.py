# Generated by Django 5.0.4 on 2024-05-18 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fams", "0003_publication_year"),
    ]

    operations = [
        migrations.AddField(
            model_name="experience",
            name="department",
            field=models.CharField(default="Computer Applications", max_length=225),
        ),
    ]
