# Generated by Django 4.1.2 on 2022-11-03 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0005_remove_images_category_images_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image1',
            field=models.ImageField(default=1, upload_to='media'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='image2',
            field=models.ImageField(default=1, upload_to='media'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='image3',
            field=models.ImageField(default=1, upload_to='media'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='image4',
            field=models.ImageField(default=1, upload_to='media'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Images',
        ),
    ]