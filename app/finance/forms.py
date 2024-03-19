from common.forms import DocumentForm
from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from .models import Product


class ProductForm(DocumentForm):
    name = forms.CharField()
    price = forms.CharField()
    date = forms.DateField(widget=AdminDateWidget)

    class Meta:
        fields = ['name', 'price', 'date']
        model = Product
