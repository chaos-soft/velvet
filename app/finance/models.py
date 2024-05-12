from django.db import models


class Product(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=100)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name
