from django.apps import AppConfig


class BookmarksConfig(AppConfig):
    name = 'bookmarks'

    def ready(self):
        from . import signals
