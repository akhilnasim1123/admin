# Generated by Django 4.1.2 on 2022-11-28 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0030_orderitems_discound'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_off',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]