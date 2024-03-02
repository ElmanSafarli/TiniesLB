from django.views.generic import TemplateView, DetailView
from .models import Product, BrandCategory
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q

class HomePage(TemplateView):
    template_name = 'pages/home.html'



class AllProducts(TemplateView):
    template_name = 'pages/all_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()

        # Retrieve all products
        products = Product.objects.all()

        # Get unique values for product brand and age category
        unique_brand = products.values_list('product_brand', flat=True).distinct()
        unique_age = products.values_list('age_category', flat=True).distinct()

        # Get filters from query parameters
        brand_filter = self.request.GET.get('brand')
        age_filter = self.request.GET.get('age')
        search_query = self.request.GET.get('q')

        print(brand_filter,age_filter)

        # Apply filters
        if brand_filter:
            products = products.filter(product_brand=brand_filter)
        if age_filter:
            products = products.filter(age_category=age_filter)

        # Apply search filter for both name and category
        if search_query:
            products = products.filter(
                Q(header__icontains=search_query) | Q(product_brand__icontains=search_query)
            )

        # Apply sorting
        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            products = products.order_by(sort_by)

        context['products'] = products
        context['unique_brands'] = unique_brand
        context['unique_age_categories'] = unique_age
        context['search_query'] = search_query

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

class BrandAll(TemplateView):
    template_name = 'pages/all_brands.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_categories = BrandCategory.objects.all()
        context['all_categories'] = all_categories
        return context


def checkout_view(request):
    return render(request, 'pages/checkout.html')

@csrf_exempt
def send_to_telegram_view(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body)
            contact_details = received_data.get('contact', {})
            cart_items = received_data.get('cart', [])

            print(cart_items)

            # Prepare the message for Telegram
            message = f"New Order Details:\n\nContact Information:\nName: {contact_details.get('name')}\nSurname: {contact_details.get('surname')}\nNumber: {contact_details.get('number')}\nAddress: {contact_details.get('address')}\n\nOrdered Items:\n"

            # Include details about the selected products
            for item in cart_items:
                product_name = item.get('name', '')
                product_price = item.get('price', 0.0)
                product_quantity = item.get('quantity', 0)

                message += f"Product: {product_name}\nPrice: ${product_price}\nQuantity: {product_quantity}\n\n"

            # Send message to Telegram
            send_to_telegram(message)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f'Error processing the order: {str(e)}')  # Debug print
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



def send_to_telegram(message):
    bot_token = '7175554526:AAHnZJxRFuXtE8AEBPBc9pGDU5I3gHxuJIk'
    chat_id = '-1001915097883'

    telegram_api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message,
    }

    response = requests.post(telegram_api_url, params=params)

    if response.status_code != 200:
        print(f"Failed to send message to Telegram. Status code: {response.status_code}")