# Generated by Django 4.1.2 on 2022-12-08 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_alter_ordereditems_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordereditems',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('delivered', 'delivered'), ('out for shipping', 'out for shipping'), ('completed', 'completed')], default='pending', max_length=20),
        ),
    ]
