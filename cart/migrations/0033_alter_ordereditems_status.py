# Generated by Django 4.1.2 on 2022-12-01 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0032_alter_ordereditems_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordereditems',
            name='status',
            field=models.CharField(choices=[('delivered', 'delivered'), ('pending', 'pending'), ('completed', 'completed'), ('out for shipping', 'out for shipping')], default='pending', max_length=20),
        ),
    ]
