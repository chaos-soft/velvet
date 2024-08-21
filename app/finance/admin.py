from common.admin import Admin
from django.contrib import admin

from .models import Product


class ProductAdmin(Admin):
    fields = ['name', 'price', 'date']
    list_display = [
        'id',
        '__str__',
        'price',
        'date',
    ]
    list_display_links = ['id', '__str__']


admin.site.register(Product, ProductAdmin)
