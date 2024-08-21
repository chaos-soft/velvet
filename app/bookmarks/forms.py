from common.forms import Form
from common.functions import get_html_title, get_thumbnail, take_screenshot
from django import forms
from django.db import models

from .models import Bookmark, Category


class BookmarkForm(Form):
    class Screenshot(models.IntegerChoices):
        EMPTY = 0, '-' * 9
        FULL = 1, 'full'
        HEIGHT = 1024, '1024'
        YOUTUBE_DL = 2, 'youtube-dl'

    UPLOAD_TO = 'bookmarks/%Y/%m/%d/'
    screenshot = forms.TypedChoiceField(required=False, choices=Screenshot.choices, coerce=int)

    class Meta:
        fields = ['title', 'urls', 'screenshot', 'category', 'images']
        model = Bookmark

    def clean(self):
        cd = super().clean()
        if self.errors:
            return cd
        cd['images'] = list(filter(None, cd['images'].split('\r\n')))
        cd['urls'] = list(filter(None, cd['urls'].split('\r\n')))
        self.xclean_screenshot()
        self.xclean_title()
        cd['images'] = '\r\n'.join(cd['images'])
        cd['urls'] = '\r\n'.join(cd['urls'])
        return cd

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
