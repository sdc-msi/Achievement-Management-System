# Generated by Django 5.0.6 on 2024-05-19 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fams", "0004_experience_department"),
    ]

    operations = [
        migrations.AddField(
            model_name="publication",
            name="doi",
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
    ]
