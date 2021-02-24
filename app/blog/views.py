from django.views.generic import DetailView, ListView

from .models import Article


class ArticleView(DetailView):
    http_method_names = ['get']
    model = Article


class ArticlesView(ListView):
    http_method_names = ['get']
    paginate_by = 10
    queryset = Article.objects.filter(is_published=True)
