# Generated by Django 5.0.3 on 2024-03-08 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0004_rename_client_id_purchase_client_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='purchase_date',
        ),
    ]