from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'id',
            'article_type',
            'cover',
            'date',
            'get_code',
            'get_intro',
            'images_list',
            'is_published',
            'title',
            'get_content',
        ]
        model = Article
