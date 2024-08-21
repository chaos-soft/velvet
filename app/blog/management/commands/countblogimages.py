from blog.models import Article
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        total = 0
        for article in Article.objects.all().iterator():
            total += len(article.images_list)
        self.stdout.write(f'{total}')
