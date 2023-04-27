from django.urls import path
from rest_framework import routers

from .views import ArticlesViewSet, SitemapView

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'api/articles', ArticlesViewSet)
urlpatterns = router.urls + [
    path('sitemap', SitemapView.as_view(), name='sitemap'),
]
