# Generated by Django 5.0.3 on 2024-03-08 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0003_rename_client_purchase_client_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='client_id',
            new_name='client',
        ),
        migrations.RenameField(
            model_name='purchase',
            old_name='product_id',
            new_name='product',
        ),
    ]
