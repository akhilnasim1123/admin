# Generated by Django 4.1.2 on 2022-11-28 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0026_alter_ordereditems_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordereditems',
            name='status',
            field=models.CharField(choices=[('completed', 'completed'), ('delivered', 'delivered'), ('out for shipping', 'out for shipping'), ('pending', 'pending')], default='pending', max_length=20),
        ),
    ]