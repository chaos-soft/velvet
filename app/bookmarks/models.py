from common.models import Model
from django.db import models


class Bookmark(Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    date = models.DateTimeField('date created', auto_now_add=True, blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True)
    urls = models.TextField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title


class Category(models.Model):
    level = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'-- {self.name}' if self.parent_id else self.name
