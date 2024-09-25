from django.urls import path
from rest_framework import routers

from .views import ArticlesViewSet, SitemapView, ArticlesView, ArticleView

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'api/articles', ArticlesViewSet, basename='articles')
urlpatterns = router.urls + [
    path('', ArticlesView.as_view(), name='articles'),
    path('articles/<int:pk>', ArticleView.as_view(), name='article'),
    path('sitemap', SitemapView.as_view(), name='sitemap'),
]
