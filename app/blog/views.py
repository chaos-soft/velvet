from django.views.generic import ListView
from rest_framework import viewsets, mixins

from .models import Article
from .serializers import ArticleSerializer


class ArticlesViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(is_published=True)
        return self.queryset


class SitemapView(ListView):
    http_method_names = ['get']
    paginate_by = 50000
    queryset = Article.objects.filter(is_published=True)
    template_name = 'blog/sitemap.html'
