from datetime import datetime

from django.contrib.admin.sites import AdminSite
from django.core.files.storage import default_storage
from django.test import SimpleTestCase

from .admin import BookmarkAdmin
from . import forms
from .models import Bookmark, Category
from .signals import category_post_save, bookmark_post_delete


class CategoryTest(Category):
    def save(self, *args, **kwargs):
        pass


class BookmarkForm(forms.BookmarkForm):
    class Meta:
        fields = ['title', 'urls', 'screenshot']
        model = Bookmark


class BookmarksTest(SimpleTestCase):
    def setUp(self):
        self.category1 = CategoryTest(id=1, name='q0t')
        self.category2 = CategoryTest(id=2, name='haokx9', parent=self.category1, parent_id=1)

        self.bookmark1 = Bookmark(id=1, category=self.category2)
        self.bookmark1.title = 'c5j'
        self.bookmark1.urls = ['hda', 'n0k']

        self.bookmark2 = Bookmark(category=self.category1)

    def test_admin(self):
        admin = BookmarkAdmin(Bookmark, AdminSite)
        self.assertEqual(admin.title(self.bookmark1),
                         '<a href="hda">c5j</a><br><a href="n0k">02</a>')
        self.assertEqual(admin.get_category(self.bookmark1), 'q0t/haokx9')
        self.assertEqual(admin.get_category(self.bookmark2), 'q0t')

    def test_forms(self):
        post = {'urls': 'https://57st.net/articles/125\r\nv5i'}
        form = BookmarkForm(post, instance=self.bookmark1)
        self.assertEqual(form.initial['urls'], 'hda\r\nn0k')
        self.assertTrue(form.is_valid())
        form.save(commit=False)
        self.assertEqual(self.bookmark1.urls, ['https://57st.net/articles/125', 'v5i'])
        self.assertEqual(self.bookmark1.title, 'Retrowave')
        post['title'] = 'poh'
        form = BookmarkForm(post, instance=self.bookmark2)
        self.assertTrue(form.is_valid())
        form.save(commit=False)
        self.assertEqual(self.bookmark2.date.date(), datetime.today().date())
        form = BookmarkForm({})
        self.assertFalse(form.is_valid())
        self.xtest_forms_xclean_screenshot(post)

    def test_models(self):
        self.assertEqual(str(self.category1), 'q0t')
        self.assertEqual(str(self.category2), '-- haokx9')
        self.assertEqual(str(self.bookmark1), 'c5j')

    def xtest_forms_xclean_screenshot(self, post):
        post['screenshot'] = BookmarkForm.Screenshot.HEIGHT
        form = BookmarkForm(post, instance=self.bookmark1)
        self.assertTrue(form.is_valid())
        form.save(commit=False)
        self.assertEqual(len(self.bookmark1.images), 1)
        self.assertTrue(default_storage.exists(self.bookmark1.images[0]))
        post['urls'] = 'https://www.youtube.com/watch?v=ljvvHgb1h_4'
        post['screenshot'] = BookmarkForm.Screenshot.YOUTUBE_DL
        post['images'] = self.bookmark1.images[0]
        form = BookmarkForm(post, instance=self.bookmark1)
        self.assertTrue(form.is_valid())
        form.save(commit=False)
        self.assertEqual(len(self.bookmark1.images), 2)
        self.assertTrue(default_storage.exists(self.bookmark1.images[-1]))
        self.xtest_signals()

    def xtest_signals(self):
        bookmark_post_delete(self.bookmark1)
        for name in self.bookmark1.images:
            self.assertFalse(default_storage.exists(name))
        category_post_save(self.category1)
        self.assertEqual(self.category1.level, 1)
        category_post_save(self.category2)
        self.assertEqual(self.category2.level, '1-haokx')
