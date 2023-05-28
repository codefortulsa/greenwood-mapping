# Generated by Django 4.2.1 on 2023-05-07 16:55

from django.db import migrations, models
import django.db.models.deletion
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pghistory", "0005_events_middlewareevents"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("entities", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EntityEvent",
            fields=[
                ("pgh_id", models.AutoField(primary_key=True, serialize=False)),
                ("pgh_created_at", models.DateTimeField(auto_now_add=True)),
                ("pgh_label", models.TextField(help_text="The event label.")),
                ("id", models.IntegerField()),
                ("name", models.CharField(max_length=120)),
                ("meta", models.JSONField(blank=True, default=dict)),
            ],
            options={
                "abstract": False,
            },
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="entity",
            trigger=pgtrigger.compiler.Trigger(
                name="protect_deletes",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func="RAISE EXCEPTION 'pgtrigger: Cannot delete rows from % table', TG_TABLE_NAME;",
                    hash="7e42d529581adb39ead3b90aeb5bcdcf0b010c17",
                    operation="DELETE",
                    pgid="pgtrigger_protect_deletes_0bd2b",
                    table="entities_entity",
                    when="BEFORE",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="entity",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "entities_entityevent" ("canonical_id", "id", "meta", "name", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "polymorphic_ctype_id") VALUES (NEW."canonical_id", NEW."id", NEW."meta", NEW."name", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."polymorphic_ctype_id"); RETURN NULL;',
                    hash="e482f6d7c0d4e27e40163d8f38d7cd271e9ad68f",
                    operation="INSERT",
                    pgid="pgtrigger_snapshot_insert_39471",
                    table="entities_entity",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="entity",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition="WHEN (OLD.* IS DISTINCT FROM NEW.*)",
                    func='INSERT INTO "entities_entityevent" ("canonical_id", "id", "meta", "name", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "polymorphic_ctype_id") VALUES (NEW."canonical_id", NEW."id", NEW."meta", NEW."name", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."polymorphic_ctype_id"); RETURN NULL;',
                    hash="30bb6f3c3d02ebf251a4709257418a0511f74f3b",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_1d8e4",
                    table="entities_entity",
                    when="AFTER",
                ),
            ),
        ),
        migrations.AddField(
            model_name="entityevent",
            name="canonical",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                related_query_name="+",
                to="entities.entity",
            ),
        ),
        migrations.AddField(
            model_name="entityevent",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AddField(
            model_name="entityevent",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="event",
                to="entities.entity",
            ),
        ),
        migrations.AddField(
            model_name="entityevent",
            name="polymorphic_ctype",
            field=models.ForeignKey(
                db_constraint=False,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                related_query_name="+",
                to="contenttypes.contenttype",
            ),
        ),
    ]
