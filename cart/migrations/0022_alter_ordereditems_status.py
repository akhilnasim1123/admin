# Generated by Django 4.1.2 on 2022-11-28 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0021_remove_ordereditems_category_offer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordereditems',
            name='status',
            field=models.CharField(choices=[('out for shipping', 'out for shipping'), ('completed', 'completed'), ('pending', 'pending')], default='pending', max_length=20),
        ),
    ]
