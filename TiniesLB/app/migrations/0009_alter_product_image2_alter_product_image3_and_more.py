# Generated by Django 5.0.2 on 2024-03-15 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
    ]
