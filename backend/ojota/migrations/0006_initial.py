# Generated by Django 5.1.1 on 2024-10-31 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ojota', '0005_delete_inventory_delete_returns_delete_sales'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productid', models.IntegerField()),
                ('serialnumber', models.CharField(blank=True, max_length=50, null=True)),
                ('staffid', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Returns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderid', models.DecimalField(decimal_places=0, max_digits=20)),
                ('productid', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('action', models.CharField(choices=[('Replace', 'Replace'), ('Refund', 'Refund')], max_length=7)),
                ('staffid', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderid', models.IntegerField()),
                ('ordersrc', models.CharField(choices=[('Facebook', 'Facebook'), ('Instagram', 'Instagram'), ('Twitter', 'Twitter'), ('Website', 'Website'), ('On premises', 'On premises')], max_length=15)),
                ('productid', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('staffid', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
