import argparse
import csv
import sys

from blog.models import Article
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                            default=sys.stdin)

    def handle(self, *args, **options):
        reader = csv.reader(options['infile'], delimiter=',')
        for row in reader:
            article = Article.objects.get(pk=row[3])
            article.images += [row[1]]
            article.save()
