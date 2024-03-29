from django.db import models
from django.utils.text import slugify
from colorfield.fields import ColorField


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    background_image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    header = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image1 = models.ImageField(upload_to='product_images/')
    image2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    description = models.TextField()
    company_name = models.CharField(max_length=255)
    product_brand = models.CharField(max_length=255)
    age_category = models.CharField(max_length=20)
    in_stock = models.BooleanField(default=True)
    colors = models.ManyToManyField('Color', blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.header)
        super().save(*args, **kwargs)

class Color(models.Model):
    # hex_code = models.CharField(max_length=7)
    color = ColorField()

    def __str__(self):
        return self.color


class BrandCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    background_image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=40, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
