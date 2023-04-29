from django.shortcuts import render
from .models import Product, Category

# Create your views here.


def all_products(request):
    """ A view to show all products, imcluding sorting and search queries """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)