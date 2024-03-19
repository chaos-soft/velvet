from datetime import datetime

from common.models import Document
from django.db import models


class Bookmark(Document):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    title = ''
    urls: list[str] = list()
    date = ''

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_types_dump(self):
        return {'date': str}

    def get_types_load(self):
        return {'date': datetime.fromisoformat}


class Category(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True,
                               null=True)

    def __str__(self):
        return f'-- {self.name}' if self.parent_id else self.name
