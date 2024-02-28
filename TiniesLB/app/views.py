from django.views.generic import TemplateView, DetailView
from .models import Product, Cart
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.db.models import Sum

class HomePage(TemplateView):
    template_name = 'pages/home.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['products'] = Product.objects.all()
    #
    #     # Fetch cart items and total price
    #     cart_items, total_price, total_quantity = get_cart_items(self.request)
    #
    #     context['cart_items'] = cart_items
    #     context['total_price'] = total_price
    #     context['total_quantity'] = total_quantity
    #     return context


class AllProducts(TemplateView):
    template_name = 'pages/all_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()

        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'pages/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()

        return context




# def checkout(request):
#     # Get products, total price, and total quantity from the user's cart
#     cart_items, total_price, total_quantity = get_cart_items(request)
#
#     context = {'cart_items': cart_items, 'total_price': total_price}
#     return render(request, 'pages/checkout.html', context)


