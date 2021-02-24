from common.models import Document
from django.db import models


class Bookmark(Document):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    title = ''
    urls = None
    date = ''

    class Meta:
        ordering = ['-id']

    def __init__(self, *args, **kwargs):
        self.urls = []
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True,
                               null=True)

    def __str__(self):
        return f'-- {self.name}' if self.parent_id else self.name
