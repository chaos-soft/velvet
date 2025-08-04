from common.admin import Admin
from django.contrib import admin

from .forms import ArticleForm
from .models import Article


class ArticleAdmin(Admin):
    form = ArticleForm
    list_display = [
        'id',
        '__str__',
        'is_comments',
        'is_published',
        'article_type',
        'status',
        'date_modified',
        'date',
        'get_cover',
    ]
    list_display_links = ['id', '__str__']
    search_fields = ['id', 'content']

    class Media:
        js = ['admin_blog.js']


admin.site.register(Article, ArticleAdmin)
