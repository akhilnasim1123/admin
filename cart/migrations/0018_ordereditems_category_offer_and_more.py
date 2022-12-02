# Generated by Django 4.1.2 on 2022-11-28 04:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0029_remove_product_discound_price'),
        ('cart', '0017_alter_ordereditems_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordereditems',
            name='category_offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='proj.categoryoffer'),
        ),
        migrations.AddField(
            model_name='ordereditems',
            name='discound_price',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='ordereditems',
            name='product_offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='proj.productoffer'),
        ),
        migrations.AlterField(
            model_name='ordereditems',
            name='status',
            field=models.CharField(choices=[('completed', 'completed'), ('out for shipping', 'out for shipping'), ('pending', 'pending')], default='pending', max_length=20),
        ),
    ]