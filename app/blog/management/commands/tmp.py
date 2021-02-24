from blog.models import Article
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for article in Article.objects.all().iterator():
            if article.cover:
                print(article.cover)
            if article.cover[:2] == '//':
                article.document['cover'] = f'https:{article.cover}'
                # article.save()
