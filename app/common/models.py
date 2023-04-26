from django.db import models

from .tipizator import INSTANCE as tipizator


class Document(models.Model):
    document = models.JSONField(default=dict)
    images: list[str] = list()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.id:
            if hasattr(self, 'get_types_load'):
                tipizator.types_load = self.get_types_load()
                self.document = tipizator.load(self.document)
            for k in self.document:
                if hasattr(self, k):
                    setattr(self, k, self.document[k])
                else:
                    raise KeyError

    def save(self, *args, **kwargs):
        if hasattr(self, 'get_types_dump'):
            tipizator.types_dump = self.get_types_dump()
            self.document = tipizator.dump(self.document)
        return super().save(*args, **kwargs)
