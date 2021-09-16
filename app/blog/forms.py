from datetime import datetime

from common.forms import DocumentForm
from common.functions import create_thumbnail, delete_thumbnail
from django import forms
from django.conf import settings
from django.utils.dateformat import format

from .models import Article


class ArticleForm(DocumentForm):
    UPLOAD_TO = 'blog/%Y/%m/%d/'
    title = forms.CharField()
    content = forms.CharField(required=False, widget=forms.Textarea)
    is_comments = forms.BooleanField(required=False)
    is_published = forms.BooleanField(required=False)
    type = forms.TypedChoiceField(choices=Article.Type.choices, coerce=int)
    cover = forms.CharField(required=False)
    code = forms.CharField(required=False, widget=forms.Textarea)
    get_youtube_image = forms.BooleanField(required=False)
    status = forms.CharField(required=False)

    class Meta:
        fields = [
            'title',
            'content',
            'is_comments',
            'is_published',
            'type',
            'cover',
            'code',
            'get_youtube_image',
            'status',
        ]
        model = Article

    def clean(self):
        cd = super().clean()
        cd['date_modified'] = format(datetime.today(), settings.DATETIME_FORMAT)
        return cd

    def delete_image(self, i):
        delete_thumbnail(self.cleaned_data['images'][i])
        super().delete_image(i)

    def upload_image(self, image):
        name = super().upload_image(image)
        create_thumbnail(name)
        return name
