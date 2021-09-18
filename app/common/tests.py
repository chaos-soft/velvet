from django import forms
from django.test import SimpleTestCase

from .functions import get_html_title, make_request


class CommonTest(SimpleTestCase):
    def test_functions(self):
        with self.assertRaises(forms.ValidationError):
            make_request('gln')
        self.assertEqual(get_html_title('https://57st.net/articles/125'), 'Retrowave')


# 3pmptqpxj2bukwkzcls3o8zy4fts7das3juhseoctmmv0
