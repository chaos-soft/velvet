from common.models import Document
from django.db import models


class Product(Document):
    date = models.DateField()
    name = ''
    price = ''

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name
