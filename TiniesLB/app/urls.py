from django.urls import path
from .views import HomePage, AllProducts, ProductDetail, checkout_view, send_to_telegram_view, BrandAll

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('products/', AllProducts.as_view(), name='all'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('brands/', BrandAll.as_view(), name='brand_categories'),
    path('checkout/', checkout_view, name='checkout'),
    path('send-to-telegram/', send_to_telegram_view, name='send_to_telegram'),
]
