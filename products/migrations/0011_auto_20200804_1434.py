# Generated by Django 3.0.8 on 2020-08-04 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20200804_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='has_sizes',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
