# Generated by Django 4.1.2 on 2022-12-10 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0005_alter_product_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=100),
        ),
    ]
