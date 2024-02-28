from django.urls import path
from .views import HomePage, AllProducts, ProductDetail

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('products/', AllProducts.as_view(), name='all'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
]
