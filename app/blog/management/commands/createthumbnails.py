from common.functions import create_thumbnail
from django.core.management.base import BaseCommand

from blog.models import Article


class Command(BaseCommand):
    def handle(self, *args, **options):
        for article in Article.objects.all().iterator():
            for name in article.images_list:
                create_thumbnail(name)
