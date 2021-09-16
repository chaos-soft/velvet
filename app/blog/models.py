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
    date_modified = ''

    class Meta:
        ordering = ['-date']

    class Type(models.IntegerChoices):
        ARTICLE = 1
        YOUTUBE = 2
        ALBUM = 4
        STREAM = 5

    def __str__(self):
        return self.title

    def command_color(self, values):
        for v in values[1:]:
            self.content = self.content.replace(v, f'<span class="color{values[0]}">{v}</span>')

    def command_replace(self, values):
        self.content = self.content.replace(*values)

    def get_absolute_url(self):
        return reverse('article', args=[self.id])

    def get_code_configparser(self):
        config = configparser.ConfigParser()
        config.read_string(f'[6bb]\r\n{self.code}')
        return config['6bb']

    def get_code_csv(self):
        return self.code.replace('\r\n', ',')

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
        if self.cover or not self.images:
            image = self.cover
        else:
            image = self.images[-1]
        if image and image[0] not in ['/', 'h']:
            image = f'/store/thumbnails/{image}'
        return image

    def get_intro(self):
        return self.content.split('\r\n', 1)[0]
