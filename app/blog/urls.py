from django.urls import path
from django.views.generic.base import RedirectView

from .views import ArticlesView, ArticleView

urlpatterns = [
    path('', ArticlesView.as_view(), name='articles'),
    path('a/<int:pk>', RedirectView.as_view(pattern_name='article', permanent=True)),
    path('articles/<int:pk>', ArticleView.as_view(), name='article'),
]
