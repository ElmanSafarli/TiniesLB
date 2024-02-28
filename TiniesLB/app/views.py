from django.views.generic import TemplateView, DetailView
from .models import Product, Cart
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.db.models import Sum

class HomePage(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()

        # Fetch cart items and total price
        cart_items, total_price, total_quantity = get_cart_items(self.request)

        context['cart_items'] = cart_items
        context['total_price'] = total_price
        context['total_quantity'] = total_quantity
        return context


class AllProducts(TemplateView):
    template_name = 'pages/all_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()

        # Fetch cart items and total price
        cart_items, total_price, total_quantity = get_cart_items(self.request)

        context['cart_items'] = cart_items
        context['total_price'] = total_price
        context['total_quantity'] = total_quantity
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'pages/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()

        # Fetch cart items and total price
        cart_items, total_price, total_quantity = get_cart_items(self.request)

        context['cart_items'] = cart_items
        context['total_price'] = total_price
        context['total_quantity'] = total_quantity
        return context


def get_cart_items(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        session_id = request.session.session_key
        cart_items = Cart.objects.filter(session_id=session_id)

    total_price = cart_items.aggregate(Sum('product__price'))['product__price__sum'] or 0
    total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0

    return cart_items, total_price, total_quantity



@require_POST
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    quantity = int(request.GET.get('quantity', 1))

    if request.user.is_authenticated:
        user = request.user
        session_id = None
    else:
        # For anonymous users, use session_key to identify the cart
        session_id = request.session.session_key
        user = None

    cart_item, created = Cart.objects.get_or_create(user=user, session_id=session_id, product=product)

    if not created:
        cart_item.quantity += quantity
        cart_item.save()


    return JsonResponse({'status': 'success'})

@require_POST
def remove_from_cart(request, product_id):
    try:
        if request.user.is_authenticated:
            # If the user is authenticated, remove the product from the cart for the user
            cart_item = Cart.objects.get(user=request.user, product__id=product_id)
        else:
            # If the user is anonymous, remove the product from the cart using the session ID
            session_id = request.session.session_key
            cart_item = Cart.objects.get(session_id=session_id, product__id=product_id)

        # Remove the cart item
        cart_item.delete()

        return JsonResponse({'status': 'success'})
    except Cart.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found in the cart'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def checkout(request):
    # Get products, total price, and total quantity from the user's cart
    cart_items, total_price, total_quantity = get_cart_items(request)

    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'pages/checkout.html', context)


