from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.test import SimpleTestCase
from django.urls import reverse
from django.utils.datastructures import MultiValueDict
from rest_framework import status
from rest_framework.test import APITestCase

from .forms import ArticleForm
from .models import Article
from .signals import post_delete


class BlogAPITest(APITestCase):
    def test_api(self):
        r = self.client.get(reverse('articles-list'))
        self.assertEqual(r.data['count'], 0)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.client.get(reverse('articles-detail', kwargs={'pk': 1}))
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)


class BlogTest(SimpleTestCase):
    def setUp(self):
        self.article1 = Article()
        self.article1.article_type = Article.Type.ARTICLE
        self.article1.title = '6wo'

        self.article2 = Article(
            article_type=Article.Type.YOUTUBE,
            cover='nsi',
            id=2,
            images='g0q\r\neyf',
            title='csf',
        )

        self.article3 = Article(images='3j5\r\nmls\r\n1dc')
        self.article3.article_type = Article.Type.YOUTUBE
        self.article3.code = 'ksu\r\nete'
        self.article3.content = 'mif\r\nbn8'

    def test_forms(self):
        post = {
            'article_type': Article.Type.ALBUM,
            'content': self.article3.content,
            'images': self.article3.images,
            'title': 'oys',
        }
        self.xtest_forms_upload_image(post)
        post['images'] = self.article3.images
        post['images_delete'] = 3
        self.xtest_forms_delete_image(post)

    def test_models(self):
        self.assertEqual(str(self.article1), '6wo')
        self.assertEqual(str(self.article2), 'csf')
        self.assertEqual(self.article3.get_code(), 'ksu,ete')
        self.assertEqual(self.article3.get_intro(), 'mif')
        self.assertEqual(self.article1.get_cover(), '')
        self.assertEqual(self.article2.get_cover(), '/store/thumbnails/nsi')
        self.assertEqual(self.article3.get_cover(), '/store/thumbnails/1dc')

    def test_signals(self):
        name = 'cc1.bje'
        thumbnail_name = f'thumbnails/{name}'
        file = SimpleUploadedFile(name, b'q8c')
        default_storage.save(name, file)
        default_storage.save(thumbnail_name, file)
        self.assertTrue(default_storage.exists(name))
        self.assertTrue(default_storage.exists(thumbnail_name))
        self.article2.images_list += [name]
        post_delete(self.article2)
        self.assertFalse(default_storage.exists(name))
        self.assertFalse(default_storage.exists(thumbnail_name))

    def xtest_forms_delete_image(self, post):
        name = self.article3.images_list[-1]
        form = ArticleForm(post, instance=self.article3)
        self.assertTrue(form.is_valid())
        self.article3 = form.save(commit=False)
        self.assertEqual(len(self.article3.images_list), 3)
        self.assertFalse(default_storage.exists(name))
        self.assertFalse(default_storage.exists(f'thumbnails/{name}'))

    def xtest_forms_upload_image(self, post):
        with (
            open(default_storage.path('images/ariel_09328_1.jpg'), 'rb') as f1,
            TemporaryUploadedFile('guk.txt', 'text/plain', 12345, 'utf8') as f2,
        ):
            f2.write(f1.read())
            files = MultiValueDict({'images_upload': [f2]})
            form = ArticleForm(post, files, instance=self.article3)
            self.assertTrue(form.is_valid())
            self.article3 = form.save(commit=False)
            self.assertEqual(len(self.article3.images_list), 4)
            name = self.article3.images_list[-1]
            self.assertTrue(default_storage.exists(name))
            self.assertTrue(default_storage.exists(f'thumbnails/{name}'))
