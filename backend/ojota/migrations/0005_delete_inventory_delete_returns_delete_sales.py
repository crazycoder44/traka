# Generated by Django 5.1.1 on 2024-10-31 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ojota', '0004_alter_inventory_serialnumber'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Inventory',
        ),
        migrations.DeleteModel(
            name='Returns',
        ),
        migrations.DeleteModel(
            name='Sales',
        ),
    ]
