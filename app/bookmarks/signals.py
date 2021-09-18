from django.core.files.storage import default_storage
from django.db.models import signals


def bookmark_post_delete(instance, **kwargs):
    for name in instance.images:
        default_storage.delete(name)


def category_post_save(instance, **kwargs):
    if instance.parent_id:
        level = f'{instance.parent_id}-{instance.name[:5]}'
    else:
        level = instance.id
    if instance.level != level:
        instance.level = level
        instance.save(update_fields=['level'])


signals.post_delete.connect(bookmark_post_delete, sender='bookmarks.Bookmark')
signals.post_save.connect(category_post_save, sender='bookmarks.Category')
