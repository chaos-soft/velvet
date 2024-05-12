from common.forms import Form
from common.functions import create_thumbnail, delete_thumbnail
from django import forms

from .models import Article


class ArticleForm(Form):
    UPLOAD_TO = 'blog/%Y/%m/%d/'
    get_youtube_image = forms.BooleanField(required=False)

    class Meta:
        fields = [
            'title',
            'content',
            'is_comments',
            'is_published',
            'article_type',
            'cover',
            'code',
            'get_youtube_image',
            'status',
            'images',
        ]
        model = Article

    def delete_image(self, i):
        delete_thumbnail(self.cleaned_data['images'][i])
        super().delete_image(i)

    def upload_image(self, image):
        name = super().upload_image(image)
        create_thumbnail(name)
        return name
