from bookmarks.models import Bookmark
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        total = 0
        for bookmark in Bookmark.objects.all().iterator():
            total += len(bookmark.images_list)
        self.stdout.write(f'{total}')
