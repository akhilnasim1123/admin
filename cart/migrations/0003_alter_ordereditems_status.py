# Generated by Django 4.1.2 on 2022-12-08 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_alter_ordereditems_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordereditems',
            name='status',
            field=models.CharField(choices=[('completed', 'completed'), ('out for shipping', 'out for shipping'), ('pending', 'pending'), ('delivered', 'delivered')], default='pending', max_length=20),
        ),
    ]
