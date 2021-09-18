from datetime import datetime

from common.forms import DocumentForm
from common.functions import get_html_title, get_thumbnail, take_screenshot
from django import forms
from django.conf import settings
from django.db import models
from django.utils.dateformat import format

from .models import Bookmark, Category


class BookmarkForm(DocumentForm):
    class Screenshot(models.IntegerChoices):
        EMPTY = 0, '-' * 9
        FULL = 1, 'full'
        HEIGHT = 1024, '1024'
        YOUTUBE_DL = 2, 'youtube-dl'

    UPLOAD_TO = 'bookmarks/%Y/%m/%d/'
    title = forms.CharField(required=False)
    urls = forms.CharField(widget=forms.Textarea)
    screenshot = forms.TypedChoiceField(required=False, choices=Screenshot.choices,
                                        coerce=int)

    class Meta:
        fields = ['title', 'urls', 'screenshot', 'category']
        model = Bookmark

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id:
            self.initial['urls'] = '\r\n'.join(self.instance.urls)

    def clean(self):
        cd = super().clean()
        if self.errors:
            return cd
        self.xclean_screenshot()
        self.xclean_title()
        if not self.instance.id:
            cd['date'] = format(datetime.today(), settings.DATETIME_FORMAT)
        return cd

    def clean_urls(self):
        self.cleaned_data['urls'] = list(filter(None, self.cleaned_data['urls'].split('\r\n')))
        return self.cleaned_data['urls']

    def xclean_screenshot(self):
        cd = self.cleaned_data
        if cd['screenshot'] in [self.Screenshot.FULL, self.Screenshot.HEIGHT]:
            name = take_screenshot(
                cd['urls'][0], self.UPLOAD_TO,
                self.Screenshot.HEIGHT if cd['screenshot'] == self.Screenshot.HEIGHT else None)
            cd['images'] += [name]
        elif cd['screenshot'] == self.Screenshot.YOUTUBE_DL:
            name = get_thumbnail(cd['urls'][0], self.UPLOAD_TO)
            cd['images'] += [name]

    def xclean_title(self):
        if not self.cleaned_data.get('title'):
            self.cleaned_data['title'] = get_html_title(self.cleaned_data['urls'][0])


class CategoryForm(forms.ModelForm):
    class Meta:
        exclude = ['level']
        model = Category

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        filter = models.Q(parent__isnull=True)
        if self.instance.id:
            filter &= ~models.Q(id=self.instance.id)
        self.fields['parent'].queryset = self.fields['parent'].queryset.filter(filter)
