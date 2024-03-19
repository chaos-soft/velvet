from datetime import datetime
import os
import subprocess

from bs4 import BeautifulSoup
from django import forms
from django.core.files.storage import default_storage
import requests

DATETIME_FORMAT = '%Y%m%d-%H%M%S'


def create_thumbnail(name, size='20000x440>'):
    args = ['convert', default_storage.path(name), '-gravity', 'center', '-thumbnail', size]
    if name[-3:] == 'jpg':
        args += ['-quality', '85']
    args += ['{path}']
    return subprocess_run(f'thumbnails/{name}', args)


def delete_thumbnail(name):
    default_storage.delete(f'thumbnails/{name}')


def get_extensions(path):
    output = subprocess.run(['file', '-b', '--extension', path], capture_output=True, text=True)
    return output.stdout.rstrip('\n')


def get_html_title(url):
    data = make_request(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    return str(soup.title.string)


def get_thumbnail(url, upload_to):
    args = ['youtube-dl', '--write-thumbnail', '--skip-download', '--output', '{path}', url]
    name = subprocess_run(f'{upload_to}{DATETIME_FORMAT}', args)
    return f'{name}.jpg'


def make_request(url, method=requests.get, timeout=60, **kwargs):
    try:
        r = method(url, timeout=timeout, **kwargs)
        r.raise_for_status()
        return r
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        raise forms.ValidationError(e, code='external')


def subprocess_run(name_format, args, is_clean=False):
    name = datetime.today().strftime(name_format)
    path = default_storage.path(name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    i = args.index('{path}')
    args[i] = path
    try:
        subprocess.run(args, check=True)
        return name
    except subprocess.CalledProcessError as e:
        if is_clean:
            default_storage.delete(name)
        raise forms.ValidationError(e, code='external')


def take_screenshot(url, upload_to, height=None):
    # --quality 0 многократно уменьшает размер PNG.
    args = ['wkhtmltoimage', '--quality', '0']
    if height:
        args += ['--height', str(height)]
    args += [url, '{path}']
    return subprocess_run(f'{upload_to}{DATETIME_FORMAT}.png', args, is_clean=True)
