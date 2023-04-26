from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.core.paginator import Paginator
from rest_framework.test import RequestsClient

from blog.models import Article
from blog.views import ArticlesView


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = RequestsClient()
        json = {}
        p = Paginator(Article.objects.filter(is_published=True), ArticlesView.paginate_by)
        for page in p.page_range:
            response = client.get(f'http://testserver/api/articles?page={page}')
            json[f'api/pages/{page}.json'] = response.text
        for article in Article.objects.all():
            response = client.get(f'http://testserver/api/articles/{article.id}')
            json[f'api/articles/{article.id}.json'] = response.text
        for name, v in json.items():
            default_storage.delete(name)
            default_storage.save(name, ContentFile(v))
