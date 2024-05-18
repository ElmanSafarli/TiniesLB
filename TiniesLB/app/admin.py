from django.contrib import admin
from .models import Product,Color, BrandCategory, Category
from import_export.admin import ImportExportModelAdmin

@admin.register(Product)
class userdat(ImportExportModelAdmin):
    list_display = ('header', 'price', 'product_brand', 'company_name', 'age_category', 'in_stock', 'description')
    search_fields = ('header', 'company_name', 'product_brand')
    list_filter = ('in_stock', 'header', 'company_name')

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('header', 'price', 'product_brand', 'company_name', 'age_category', 'in_stock', 'description')
#     search_fields = ('header', 'company_name', 'product_brand')
#     list_filter = ('in_stock', 'header', 'company_name')

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('color', )
    search_fields = ('color', )

@admin.register(BrandCategory)
class AllBrandsAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

@admin.register(Category)
class AllCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )