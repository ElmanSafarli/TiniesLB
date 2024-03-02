# Generated by Django 5.0.2 on 2024-03-02 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('background_image', models.ImageField(blank=True, null=True, upload_to='category_images/')),
            ],
        ),
    ]
