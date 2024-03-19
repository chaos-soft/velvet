from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'id',
            'images',

            'date',
            'is_published',
            'title',
            'type',
            'cover',

            'get_intro',

            'get_code',
            'get_content',
        ]
        model = Article
