import configparser

from common.models import Model
from django.db import models
import markdown


class Article(Model):
    class Type(models.IntegerChoices):
        ARTICLE = 1
        YOUTUBE = 2
        ALBUM = 4
        STREAM = 5
        RUTUBE = 6

    article_type = models.PositiveSmallIntegerField(choices=Type, default=Type.ARTICLE)
    cache_content = models.TextField()
    code = models.TextField(blank=True)
    content = models.TextField()
    cover = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    is_comments = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    status = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def command_color(self, values):
        for v in values[1:]:
            self.content = self.content.replace(v, f'<span class="color{values[0]}">{v}</span>')

    def command_replace(self, values):
        self.content = self.content.replace(*values)

    def get_code(self):
        if self.article_type == Article.Type.YOUTUBE:
            return self.code.replace('\r\n', ',')
        elif self.article_type == Article.Type.STREAM:
            config = configparser.ConfigParser()
            config.read_string(f'[6bb]\r\n{self.code}')
            return config['6bb']
        else:
            return self.code.split('\r\n')

    def get_content(self):
        commands = []
        strings = self.content.split('\r\n')
        while True:
            str_ = strings[-1]
            if str_.startswith('-') and not str_.startswith('- '):
                commands += [str_[1:]]
                del strings[-1]
            else:
                break
        self.content = markdown.markdown('\r\n'.join(strings), output_format='html5')
        for command in commands:
            name, values = command.split(' ', 1)
            getattr(self, f'command_{name}')(values.split(','))
        return self.content

    def get_cover(self):
        if self.cover or not self.images_list:
            image = self.cover
        else:
            image = self.images_list[-1]
        if image and image[0] not in ['/', 'h']:
            image = f'/store/thumbnails/{image}'
        return image

    def get_intro(self):
        return self.content.split('\r\n', 1)[0]
