from django.contrib.admin.sites import AdminSite
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from django.utils.datastructures import MultiValueDict

from .admin import ArticleAdmin
from .forms import ArticleForm
from .models import Article
from .signals import post_delete


class BlogTest(SimpleTestCase):
    def setUp(self):
        self.article1 = Article()
        self.article1.title = '6wo'
        self.article1.type = Article.Type.ARTICLE

        self.article2 = Article(id=2, document={
            'title': 'csf',
            'type': Article.Type.YOUTUBE,
            'cover': 'nsi',
            'images': ['g0q', 'eyf'],
        })

        self.article3 = Article()
        self.article3.content = 'mif\r\nbn8'
        self.article3.code = 'ksu\r\nete'
        self.article3.images = ['3j5', 'mls', '1dc']

    def test_admin(self):
        admin = ArticleAdmin(Article, AdminSite)
        self.assertEqual(admin.images(self.article1), '')
        self.assertEqual(admin.images(self.article2), '/store/thumbnails/nsi')
        self.assertEqual(admin.images(self.article3), '/store/thumbnails/1dc')
        self.assertEqual(admin.type(self.article1), Article.Type.ARTICLE.label)
        self.assertEqual(admin.type(self.article2), Article.Type.YOUTUBE.label)
        self.assertEqual(admin.get_is_comments(self.article1),
                         '<img src="/static/admin/img/icon-no.svg">')

    def test_forms(self):
        post = {
            'title': 'oys',
            'type': Article.Type.ALBUM,
            'images': '\r\n'.join(self.article3.images),
        }
        self.xtest_forms_upload_image(post)
        post['images'] = '\r\n'.join(self.article3.images)
        post['images_delete'] = 3
        self.xtest_forms_delete_image(post)

    def test_models(self):
        self.assertEqual(str(self.article1), '6wo')
        self.assertEqual(str(self.article2), 'csf')
        self.assertEqual(self.article3.get_code_csv(), 'ksu,ete')
        self.assertEqual(self.article3.get_intro(), 'mif')

    def test_signals(self):
        name = 'cc1.bje'
        thumbnail_name = f'thumbnails/{name}'
        file = SimpleUploadedFile(name, b'q8c')
        default_storage.save(name, file)
        default_storage.save(thumbnail_name, file)
        self.assertTrue(default_storage.exists(name))
        self.assertTrue(default_storage.exists(thumbnail_name))
        self.article2.images += [name]
        post_delete(self.article2)
        self.assertFalse(default_storage.exists(name))
        self.assertFalse(default_storage.exists(thumbnail_name))

    def xtest_forms_delete_image(self, post):
        name = self.article3.images[-1]
        form = ArticleForm(post, instance=self.article3)
        self.assertTrue(form.is_valid())
        form.save(commit=False)
        self.assertEqual(len(self.article3.images), 3)
        self.assertFalse(default_storage.exists(name))
        self.assertFalse(default_storage.exists(f'thumbnails/{name}'))

    def xtest_forms_upload_image(self, post):
        with open(default_storage.path('images/ariel_09328_1.jpg'), 'rb') as f:
            files = MultiValueDict(
                {'images_upload': [SimpleUploadedFile('ariel_09328_1.jpg', f.read())]})
        form = ArticleForm(post, files, instance=self.article3)
        self.assertTrue(form.is_valid())
        form.save(commit=False)
        self.assertEqual(len(self.article3.images), 4)
        name = self.article3.images[-1]
        self.assertTrue(default_storage.exists(name))
        self.assertTrue(default_storage.exists(f'thumbnails/{name}'))
