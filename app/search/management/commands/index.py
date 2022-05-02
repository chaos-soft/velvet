from collections import deque

from blog.models import Article
from bookmarks.models import Bookmark
from django.conf import settings
from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk

es = Elasticsearch(settings.ELASTICSEARCH_HOST)


def get_articles():
    for article in Article.objects.all().iterator():
        yield {
            '_id': article.id,
            '_index': 'articles',
            'title': article.title,
            'content': article.content,
        }


def get_bookmarks():
    for bookmark in Bookmark.objects.all().iterator():
        yield {
            '_id': bookmark.id,
            '_index': 'bookmarks',
            'title': bookmark.title,
            'urls': bookmark.urls,
        }


class Command(BaseCommand):
    def handle(self, *args, **options):
        es.indices.delete(index='articles,bookmarks', ignore_unavailable=True)
        deque(parallel_bulk(es, get_articles()), maxlen=0)
        deque(parallel_bulk(es, get_bookmarks()), maxlen=0)
