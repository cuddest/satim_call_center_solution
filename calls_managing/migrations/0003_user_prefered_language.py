# Generated by Django 5.0.4 on 2024-09-20 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calls_managing", "0002_administrator_admin"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="prefered_language",
            field=models.CharField(default="English", max_length=100),
        ),
    ]
