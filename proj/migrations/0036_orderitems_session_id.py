# Generated by Django 4.1.2 on 2022-12-01 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0035_alter_category_offer_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='session_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
