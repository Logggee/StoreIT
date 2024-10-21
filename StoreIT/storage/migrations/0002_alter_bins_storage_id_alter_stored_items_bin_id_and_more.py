# Generated by Django 4.2.16 on 2024-10-21 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("storage", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bins",
            name="storage_id",
            field=models.ForeignKey(
                db_column="storage_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="storages",
                to="storage.storages",
            ),
        ),
        migrations.AlterField(
            model_name="stored_items",
            name="bin_id",
            field=models.ForeignKey(
                db_column="bin_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="bins",
                to="storage.bins",
            ),
        ),
        migrations.AlterField(
            model_name="stored_items",
            name="item_id",
            field=models.ForeignKey(
                db_column="item_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="items",
                to="storage.items",
            ),
        ),
    ]
