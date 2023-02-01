# Generated by Django 4.1.5 on 2023-01-31 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('item_id', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='Price')),
                ('item_url', models.URLField(verbose_name='URL')),
                ('images', models.TextField(null=True, verbose_name='Images')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('breadcrumbs', models.TextField(null=True, verbose_name='Breadcrumbs')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Item',
            },
        ),
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_name', models.CharField(max_length=255, unique=True, verbose_name='Property')),
            ],
            options={
                'verbose_name': 'Properties',
                'verbose_name_plural': 'Properties',
            },
        ),
        migrations.CreateModel(
            name='PriceDynamic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='Price')),
                ('price_date', models.DateField(verbose_name='Date')),
                ('tmp', models.CharField(max_length=14, verbose_name='delete me')),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leoapp.items', verbose_name='Item ID')),
            ],
            options={
                'verbose_name': 'Price dynamic',
                'verbose_name_plural': 'Price dynamic',
            },
        ),
        migrations.CreateModel(
            name='ItemProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_value', models.CharField(max_length=255, null=True, verbose_name='Value')),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leoapp.items', verbose_name='Item ID')),
                ('property_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leoapp.properties', verbose_name='Property ID')),
            ],
            options={
                'verbose_name': 'Item property',
                'verbose_name_plural': 'Item property',
                'unique_together': {('property_id', 'item_id')},
            },
        ),
    ]
