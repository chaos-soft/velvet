from common.admin import DocumentAdmin
from django.contrib import admin

from .forms import ProductForm
from .models import Product


class ProductAdmin(DocumentAdmin):
    form = ProductForm
    list_display = [
        'id',
        '__str__',
        'price',
        'date',
    ]
    list_display_links = ['id', '__str__']


admin.site.register(Product, ProductAdmin)
