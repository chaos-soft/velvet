import configparser

from common.models import Document
from django.db import models
from django.urls import reverse
import markdown


class Article(Document):
    date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    title = ''
    content = ''
    is_comments = False
    type = 0
    cover = ''
    code = ''
    status = ''

    class Meta:
        ordering = ['-date']

    class Type(models.IntegerChoices):
        ARTICLE = 1
        YOUTUBE = 2
        ALBUM = 4
        STREAM = 5

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', args=[self.id])

    def get_code_configparser(self):
        config = configparser.ConfigParser()
        config.read_string(f'[6bb]\r\n{self.code}')
        return config['6bb']

    def get_code_csv(self):
        return self.code.replace('\r\n', ',')

    def get_content(self):
        return markdown.markdown(self.content, output_format='html5')

    def get_cover(self):
        if self.cover or not self.images:
            image = self.cover
        else:
            image = self.images[-1]
        if image and image[0] not in ['/', 'h']:
            image = '/store/thumbnails/' + image
        return image

    def get_intro(self):
        return self.content.split('\r\n', 1)[0]
