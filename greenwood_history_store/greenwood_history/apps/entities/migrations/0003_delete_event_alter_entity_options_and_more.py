# Generated by Django 4.2.1 on 2023-05-20 23:56

from django.db import migrations, models
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ("entities", "0002_entityevent_entity_protect_deletes_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Event",
        ),
        migrations.AlterModelOptions(
            name="entity",
            options={"ordering": ("-id",), "verbose_name_plural": "entities"},
        ),
        migrations.AlterField(
            model_name="person",
            name="name_parsed",
            field=models.BooleanField(default=False),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="entity",
            trigger=pgtrigger.compiler.Trigger(
                name="read_only_fields",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition='WHEN (OLD."name" IS DISTINCT FROM (NEW."name"))',
                    func="RAISE EXCEPTION 'pgtrigger: Cannot update rows from % table', TG_TABLE_NAME;",
                    hash="d4e0a0bbb0dcded70bb0d1e8a6fe1cd484c9aca1",
                    operation="UPDATE",
                    pgid="pgtrigger_read_only_fields_d0075",
                    table="entities_entity",
                    when="BEFORE",
                ),
            ),
        ),
    ]
