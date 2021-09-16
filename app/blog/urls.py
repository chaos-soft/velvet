from django.urls import path

from .views import ArticlesView, ArticleView

urlpatterns = [
    path('', ArticlesView.as_view(), name='articles'),
    path('articles/<int:pk>', ArticleView.as_view(), name='article'),
]
