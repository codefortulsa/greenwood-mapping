# Generated by Django 4.1.7 on 2023-04-01 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("entities", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entity",
            name="meta",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
