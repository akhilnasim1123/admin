# Generated by Django 4.1.2 on 2022-11-28 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0022_alter_ordereditems_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordereditems',
            name='status',
            field=models.CharField(choices=[('completed', 'completed'), ('pending', 'pending'), ('out for shipping', 'out for shipping')], default='pending', max_length=20),
        ),
    ]
