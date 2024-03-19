from common.admin import DocumentAdmin
from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from .forms import BookmarkForm, CategoryForm
from .models import Bookmark, Category


class BookmarkAdmin(DocumentAdmin):
    form = BookmarkForm
    list_display = ['id', 'title', 'images', 'get_category', 'date']
    list_filter = ['category']

    def get_category(self, obj):
        if obj.category.parent_id:
            return f'{obj.category.parent.name}/{obj.category.name}'
        return obj.category.name

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('category__parent')

    def title(self, obj):
        links = [(obj.urls[0], obj)]
        for i, url in enumerate(obj.urls[1:]):
            links += [(url, str(i + 2).zfill(2))]
        return format_html_join(mark_safe('<br>'), '<a href="{}">{}</a>', links)


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ['id', '__str__', 'level']
    list_display_links = ['id', '__str__']
    ordering = ['level']


admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Category, CategoryAdmin)
