from django.urls import path
from .views import HomePage, AllProducts, ProductDetail, add_to_cart, remove_from_cart, checkout

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('products/', AllProducts.as_view(), name='all'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
]
