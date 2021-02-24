import json

from django.db import models


class JSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        kwargs['ensure_ascii'] = False
        super().__init__(*args, **kwargs)


class Document(models.Model):
    document = models.JSONField(encoder=JSONEncoder, default=dict)
    images = None

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        self.images = []
        super().__init__(*args, **kwargs)
        if self.id:
            for k in self.document:
                if hasattr(self, k):
                    setattr(self, k, self.document[k])
                else:
                    raise KeyError
