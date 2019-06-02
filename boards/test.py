from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

from boards.views import home


class HomeTest(TestCase):
    def test_home_view_status_code(self):
        url = reverse('boards:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, home)