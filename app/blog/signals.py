from common.functions import delete_thumbnail
from django.core.files.storage import default_storage
from django.db.models import signals


def post_delete(instance, **kwargs):
    for name in instance.images:
        default_storage.delete(name)
        delete_thumbnail(name)


signals.post_delete.connect(post_delete, sender='blog.Article')
