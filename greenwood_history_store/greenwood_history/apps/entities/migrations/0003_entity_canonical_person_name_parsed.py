# Generated by Django 4.1.7 on 2023-04-02 23:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0002_alter_entity_meta'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='canonical',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='entities.entity'),
        ),
        migrations.AddField(
            model_name='person',
            name='name_parsed',
            field=models.BooleanField(default=True),
        ),
    ]
