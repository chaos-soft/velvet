from common.admin import DocumentAdmin
from django.contrib import admin
from django.utils.html import format_html

from .forms import ArticleForm
from .models import Article


class ArticleAdmin(DocumentAdmin):
    form = ArticleForm
    list_display = [
        'id',
        '__str__',
        'date',
        'date_modified',
        'get_is_comments',
        'is_published',
        'type',
        'status',
        'images',
    ]
    list_display_links = ['id', '__str__']

    class Media:
        js = ['admin_blog.js']

    def get_is_comments(self, obj):
        return format_html('<img src="/static/admin/img/icon-{}.svg">',
                           'yes' if obj.is_comments else 'no')

    def images(self, obj):
        return obj.get_cover()

    def type(self, obj):
        return Article.Type(obj.type).label


admin.site.register(Article, ArticleAdmin)
