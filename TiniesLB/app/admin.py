from django.contrib import admin
from .models import Product,Color, BrandCategory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('header', 'price', 'product_brand', 'company_name', 'age_category', 'in_stock', 'description')
    search_fields = ('header', 'company_name', 'product_brand')
    list_filter = ('in_stock', 'header', 'company_name')

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('hex_code', )
    search_fields = ('hex_code', )

@admin.register(BrandCategory)
class AllBrandsAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
