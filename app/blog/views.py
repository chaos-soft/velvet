from django.views.generic import ListView, DetailView
from rest_framework import viewsets, mixins

from .models import Article
from .serializers import ArticleSerializer


class ArticlesView(ListView):
    http_method_names = ['get']
    paginate_by = 10
    queryset = Article.objects.filter(is_published=True).exclude(article_type=Article.Type.HIDDEN)


class ArticlesViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        if self.action == 'list':
            return ArticlesView.queryset
        return self.queryset


class ArticleView(DetailView):
    http_method_names = ['get']
    model = Article

    def get_template_names(self):
        if self.object.template:
            return [f'blog/{self.object.Template(self.object.template).name.lower()}.html']
        else:
            return super().get_template_names()


class SitemapView(ArticlesView):
    paginate_by = 50000
    template_name = 'blog/sitemap.html'
