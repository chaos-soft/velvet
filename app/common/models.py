from django.db import models


class Model(models.Model):
    images = models.TextField(blank=True)
    images_list: list[str] = list()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.images:
            self.images_list = self.images.split('\r\n')
