# Generated by Django 4.2.16 on 2024-10-22 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("storage", "0002_alter_bins_storage_id_alter_stored_items_bin_id_and_more"),
    ]

    operations = [
        migrations.RenameModel(old_name="Bins", new_name="Bin",),
        migrations.RenameModel(old_name="Items", new_name="Item",),
        migrations.RenameModel(old_name="Storages", new_name="Storage",),
        migrations.RenameModel(old_name="Stored_Items", new_name="Stored_Item",),
    ]
