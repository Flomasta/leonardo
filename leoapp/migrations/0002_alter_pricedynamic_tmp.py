# Generated by Django 4.1.5 on 2023-02-01 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leoapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricedynamic',
            name='tmp',
            field=models.TextField(verbose_name='delete me'),
        ),
    ]
