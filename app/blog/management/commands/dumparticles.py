from django.core.management.base import BaseCommand

from blog.models import Article


class Command(BaseCommand):
    def handle(self, *args, **options):
        for article in Article.objects.all().iterator():
            self.stdout.write(f'{article}', ending='\n\n')
            self.stdout.write(f'{article.content}', ending='\n\n')
