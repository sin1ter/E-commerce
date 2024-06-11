from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import *
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.

def store(request, category_slug=None):
    cateogries = None
    products = None

    if category_slug != None:
        cateogries = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=cateogries, is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products' : paged_product,
        'product_count' : product_count, 
    }
    return render(request, 'store/store.html', context)

def product_detail(reqeust, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(reqeust), product=single_product).exists()
        
    except Exception as e:
        raise e 
    
    context = {
        'single_product' : single_product,
        'in_cart' : in_cart,
    }

    return render(reqeust, 'store/product_detail.html', context)