# Generated by Django 4.1.5 on 2023-02-02 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leoapp', '0004_remove_pricedynamic_tmp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='title',
            field=models.CharField(default='no_title', max_length=255, verbose_name='Title'),
        ),
    ]
