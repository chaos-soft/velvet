from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.core.paginator import Paginator
from django.test import RequestFactory
from django.views.generic.base import TemplateView

from blog.models import Article
from blog.views import ArticlesView, ArticleView


class Command(BaseCommand):
    def handle(self, *args, **options):
        factory = RequestFactory()
        request = factory.get('')
        html = {}
        p = Paginator(Article.objects.filter(is_published=True), ArticlesView.paginate_by)
        for page in p.page_range:
            html[f'html/pages/{page}.html'] = \
                ArticlesView.as_view()(request, page=page).render().content. \
                replace(b'/?page=', b'/pages/')
        for article in Article.objects.all().iterator():
            html[f'html/articles/{article.id}.html'] = \
                ArticleView.as_view()(request, pk=article.id).render().content
        html['html/error.html'] = \
            TemplateView.as_view(template_name='error.html')(request).render().content
        html['html/index.html'] = html['html/pages/1.html']
        for name, v in html.items():
            default_storage.delete(name)
            default_storage.save(name, ContentFile(v))
